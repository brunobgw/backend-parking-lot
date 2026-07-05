from pydantic import BaseModel, Field


class ConfiguracaoEstacionamentoSchema(BaseModel):
    """ Define como a configuração do estacionamento deve ser representada
        ao ser cadastrada ou atualizada.
    """
    area: float = Field(..., description="Área total do estacionamento, em metros quadrados", examples=[500.0])
    capacidade: int = Field(..., description="Quantidade máxima de carros que o estacionamento comporta", examples=[50])
    preco_hora: float = Field(..., description="Valor cobrado por hora de permanência", examples=[5.0])


def apresenta_configuracao(configuracao) -> dict:
    """ Retorna a representação da configuração do estacionamento
    """
    return {
        "id": configuracao.id,
        "area": configuracao.area,
        "capacidade": configuracao.capacidade,
        "preco_hora": configuracao.preco_hora,
    }
