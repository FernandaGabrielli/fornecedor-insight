import requests


def buscar_empresas(cnpj):

    # Monta URL da consulta utilizando o CNPJ informado
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"

    # Realiza requisição HTTP GET para a BrasilAPI
    response = requests.get(url)

    # Verifica se a resposta da API foi bem-sucedida
    if response.status_code == 200:

        # Retorna os dados da empresa em formato JSON
        return response.json()

    # Retorna None caso o CNPJ não seja encontrado
    # ou ocorra erro na requisição
    return None