import requests

from logger import logger

CNPJ_WS_URL = "https://publica.cnpj.ws/cnpj/{cnpj}"
TIMEOUT_SEGUNDOS = 10


class CNPJNaoEncontradoError(Exception):
    """ Lançada quando o CNPJ informado não é encontrado na base pública """


class CNPJConsultaIndisponivelError(Exception):
    """ Lançada quando não foi possível consultar o serviço público de CNPJ """


def consulta_cnpj(cnpj: str) -> dict:
    """ Consulta os dados cadastrais de uma empresa a partir do CNPJ

    Utiliza a API pública https://publica.cnpj.ws e retorna a razão social e
    os dados de contato (telefone e e-mail) cadastrados para a empresa.

    Arguments:
        cnpj: CNPJ (somente números, 14 dígitos) da empresa a ser consultada

    Raises:
        CNPJNaoEncontradoError: quando o CNPJ não é encontrado
        CNPJConsultaIndisponivelError: quando a consulta não pôde ser feita
    """
    try:
        response = requests.get(CNPJ_WS_URL.format(cnpj=cnpj), timeout=TIMEOUT_SEGUNDOS)
    except requests.RequestException as e:
        logger.warning(f"Falha ao consultar CNPJ {cnpj}: {e}")
        raise CNPJConsultaIndisponivelError("Não foi possível consultar o CNPJ no momento") from e

    if response.status_code == 404:
        raise CNPJNaoEncontradoError(f"CNPJ {cnpj} não encontrado :/")
    if response.status_code != 200:
        logger.warning(f"Consulta ao CNPJ {cnpj} retornou status {response.status_code}")
        raise CNPJConsultaIndisponivelError("Não foi possível consultar o CNPJ no momento")

    dados = response.json()
    estabelecimento = dados.get("estabelecimento") or {}

    telefone = None
    if estabelecimento.get("telefone1"):
        ddd = estabelecimento.get("ddd1")
        telefone = f"({ddd}) {estabelecimento['telefone1']}" if ddd else estabelecimento["telefone1"]

    return {
        "razao_social": dados.get("razao_social"),
        "telefone": telefone,
        "email": estabelecimento.get("email"),
    }
