import re
import os
import pandas as pd
import unicodedata
from datetime import datetime
import json
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    jsonify
)

from openpyxl import Workbook
from openpyxl.styles import Font
from io import BytesIO

# Serviço responsável por consultar dados da empresa na BrasilAPI
from services.brasil_api import buscar_empresas

# Serviço responsável pela lógica de classificação de risco
from services.risk_analyzer import calcular_risco

# Serviços responsáveis por salvar e carregar o histórico
from services.history_manager import (
    salvar_historico,
    carregar_historico
)

# Inicializa Flask
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    empresa = None

    historico = carregar_historico()


    historico.sort(
        key=lambda item: datetime.strptime(
            item["data_consulta"],
            "%d/%m/%Y %H:%M"
        ),
        reverse=True
    )

    erro = None

    if request.method == 'POST':

        cnpj = request.form.get("cnpj", "")

        # Remove máscara
        cnpj = re.sub(r"\D", "", cnpj)

        empresa = buscar_empresas(cnpj)

        if empresa:

            empresa['risco'] = calcular_risco(empresa)

            salvar_historico(empresa)

            historico = carregar_historico()

        else:

            erro = (
                "Empresa não encontrada. "
                "Verifique o CNPJ e tente novamente."
            )

    return render_template(
        'index.html',
        empresa=empresa,
        historico=historico,
        erro=erro
    )


# ==========================================
# EXPORTAR XLSX
# ==========================================

@app.route('/exportar/<cnpj>')
def exportar(cnpj):

    # Remove máscara
    cnpj = re.sub(r"\D", "", cnpj)

    # Busca empresa
    empresa = buscar_empresas(cnpj)

    if not empresa:

        return "Empresa não encontrada."

    # Calcula risco
    empresa['risco'] = calcular_risco(empresa)

    # ==========================================
    # DADOS PRINCIPAIS
    # ==========================================

    dados_empresa = {

        "Razão Social": [empresa.get("razao_social")],
        "CNPJ": [empresa.get("cnpj")],
        "Nome Fantasia": [empresa.get("nome_fantasia")],
        "Situação": [empresa.get("descricao_situacao_cadastral")],
        "Cidade": [empresa.get("municipio")],
        "UF": [empresa.get("uf")],
        "CNAE": [empresa.get("cnae_fiscal_descricao")],
        "Capital Social": [empresa.get("capital_social")],
        "Risco": [empresa.get("risco")]

    }

    df_empresa = pd.DataFrame(dados_empresa)

    # ==========================================
    # SÓCIOS
    # ==========================================

    socios = empresa.get("qsa", [])

    lista_socios = []

    for socio in socios:

        lista_socios.append({

            "Nome": socio.get("nome_socio"),
            "Qualificação": socio.get("qualificacao_socio")

        })

    df_socios = pd.DataFrame(lista_socios)

    # ==========================================
    # NOME DO ARQUIVO
    # ==========================================

    nome_empresa = empresa.get(
        "razao_social",
        "empresa"
    )

    # Remove acentos
    nome_empresa = unicodedata.normalize(
        "NFKD",
        nome_empresa
    ).encode(
        "ascii",
        "ignore"
    ).decode(
        "utf-8"
    )

    # Remove caracteres inválidos
    nome_empresa = re.sub(
        r'[^a-zA-Z0-9\s_-]',
        '',
        nome_empresa
    )

    # Troca espaços por underline
    nome_empresa = nome_empresa.replace(
        " ",
        "_"
    )

    # Evita nomes gigantes
    nome_empresa = nome_empresa[:60]

    # Nome final
    nome_arquivo = (
        f"{nome_empresa}.xlsx"
    )

    # ==========================================
    # CRIA XLSX
    # ==========================================

    with pd.ExcelWriter(
        nome_arquivo,
        engine="openpyxl"
    ) as writer:

        df_empresa.to_excel(
            writer,
            sheet_name="Empresa",
            index=False
        )

        df_socios.to_excel(
            writer,
            sheet_name="Sócios",
            index=False
        )

    # ==========================================
    # DOWNLOAD
    # ==========================================

    return send_file(
        nome_arquivo,
        as_attachment=True
    )

@app.route('/exportar-historico')
def exportar_historico():



    # Carrega histórico
    historico = carregar_historico()

    # Captura índices selecionados
    indices = request.args.get("indices")

    # Se tiver índices selecionados
    if indices:

        lista_indices = [
            int(i)
            for i in indices.split(",")
        ]

        historico = [
            historico[i]
            for i in lista_indices
        ]

    # Dados iguais da tabela HTML
    dados = []

    for item in historico:

        dados.append({

            "Data": item.get("data_consulta"),

            "Empresa": item.get("razao_social"),

            "CNPJ": item.get("cnpj"),

            "Resumo":
                f"{item.get('situacao')} - "
                f"{item.get('cnae')}",

            "Fonte": item.get("fonte"),

            "Link": item.get("link")

        })

    # Cria DataFrame
    df = pd.DataFrame(dados)

    # Arquivo em memória
    output = BytesIO()

    # Exporta XLSX
    with pd.ExcelWriter(
        output,
        engine='openpyxl'
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name='Historico'
        )

    output.seek(0)

    return send_file(

        output,

        as_attachment=True,

        download_name='historico_consultas.xlsx',

        mimetype=(
            'application/vnd.openxmlformats-officedocument.'
            'spreadsheetml.sheet'
        )

    )



@app.route("/apagar-historico", methods=["POST"])
def apagar_historico():

    dados = request.get_json()

    ids = dados.get("indices", [])

    caminho = os.path.join(
        "data",
        "historico.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:

        historico = json.load(f)

    # Remove apenas os IDs selecionados
    historico = [

        item for item in historico

        if item.get("id") not in ids

    ]

    with open(caminho, "w", encoding="utf-8") as f:

        json.dump(
            historico,
            f,
            ensure_ascii=False,
            indent=4
        )

    return jsonify({
        "success": True
    })

    dados = request.get_json()

    cnpjs = dados.get("indices", [])

    caminho = os.path.join(
        "data",
        "historico.json"
    )

    with open(caminho, "r", encoding="utf-8") as f:

        historico = json.load(f)

    # Remove os registros selecionados
    historico = [

        item for item in historico

        if item.get("cnpj") not in cnpjs

    ]

    with open(caminho, "w", encoding="utf-8") as f:

        json.dump(
            historico,
            f,
            ensure_ascii=False,
            indent=4
        )

    return jsonify({
        "success": True
    })
# Executa aplicação
if __name__ == '__main__':
    app.run(debug=True) 