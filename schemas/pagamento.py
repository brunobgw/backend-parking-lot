from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class PagamentoBuscaSchema(BaseModel):
    """ Define os filtros de busca de pagamentos recebidos
    """
    data: Optional[date] = Field(None, description="Data (AAAA-MM-DD) para filtrar os pagamentos recebidos naquele dia")


def apresenta_pagamento(pagamento) -> dict:
    """ Retorna a representação de um pagamento recebido
    """
    return {
        "id": pagamento.id,
        "numero_vaga": pagamento.numero_vaga,
        "placa": pagamento.placa,
        "valor": pagamento.valor,
        "data_hora": pagamento.data_hora.isoformat(),
    }


def apresenta_pagamentos(pagamentos: list) -> dict:
    """ Retorna a representação de uma lista de pagamentos recebidos
    """
    return {"pagamentos": [apresenta_pagamento(pagamento) for pagamento in pagamentos]}
