from datetime import datetime

def calcular_risco(empresa):

    score = 0

    # Situação cadastral
    if empresa.get("descricao_situacao_cadastral") != "ATIVA":
        score += 100

    # Capital social baixo
    capital_social = float(empresa.get("capital_social", 0))

    if capital_social < 10000:
        score += 30

    elif capital_social < 50000:
        score += 10

    # Empresa muito nova
    data_abertura = empresa.get("data_inicio_atividade")

    if data_abertura:

        ano_abertura = int(data_abertura.split("-")[0])

        idade_empresa = datetime.now().year - ano_abertura

        if idade_empresa < 1:
            score += 40

        elif idade_empresa < 5:
            score += 20

    # Classificação final
    if score >= 80:
        return "ALTO"

    elif score >= 40:
        return "MÉDIO"

    return "BAIXO"