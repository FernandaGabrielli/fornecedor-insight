
from datetime import datetime
import uuid
import os
import json

# ==========================================
# CAMINHO DO ARQUIVO JSON
# RESPONSÁVEL POR ARMAZENAR O HISTÓRICO
# ==========================================

CAMINHO = os.path.join(
    "data",
    "historico.json"
)


def carregar_historico():

    # ==========================================
    # VERIFICA SE O ARQUIVO EXISTE
    # ==========================================

    if not os.path.exists(
        CAMINHO
    ):

        # Retorna lista vazia caso
        # o arquivo ainda não exista
        return []

    # ==========================================
    # ABRE O ARQUIVO JSON EM MODO LEITURA
    # ==========================================

    with open(

        CAMINHO,

        "r",

        encoding="utf-8"

    ) as f:

        # ==========================================
        # CONVERTE JSON -> LISTA PYTHON
        # ==========================================

        return json.load(f)

def criar_resumo(empresa):
    return {
        "id": str(uuid.uuid4()),
        "data_consulta": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "razao_social": empresa.get("razao_social"),
        "cnpj": empresa.get("cnpj"),
        "situacao": empresa.get("descricao_situacao_cadastral"),
        "cnae": empresa.get("cnae_fiscal_descricao"),
        "municipio": empresa.get("municipio"),
        "uf": empresa.get("uf"),
        "risco": empresa.get("risco"),
        "fonte": "BrasilAPI",
        "link": f"https://brasilapi.com.br/api/cnpj/v1/{empresa.get('cnpj')}",
    }

def salvar_historico(empresa):
    historico = carregar_historico()

    resumo = criar_resumo(empresa)

    historico.append(resumo)

    with open(CAMINHO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)
def apagar_historico_por_ids(
    ids
):

    # ==========================================
    # CARREGA HISTÓRICO COMPLETO
    # ==========================================

    historico = (
        carregar_historico()
    )

    # ==========================================
    # REMOVE ITENS CUJO ID ESTEJA
    # NA LISTA RECEBIDA
    # ==========================================

    historico = [

        item for item in historico

        if item.get("id") not in ids

    ]

    # ==========================================
    # SALVA HISTÓRICO ATUALIZADO
    # ==========================================

    with open(

        CAMINHO,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            historico,

            f,

            ensure_ascii=False,

            indent=4

        )