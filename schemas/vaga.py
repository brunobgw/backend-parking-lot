from pydantic import BaseModel, Field


class VagaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca de uma vaga,
        feita com base no número da vaga.
    """
    numero: int = Field(..., description="Número da vaga")


class VagaOcupacaoSchema(BaseModel):
    """ Define os dados necessários para ocupar uma vaga
    """
    placa: str = Field(..., description="Placa do veículo que irá ocupar a vaga", examples=["ABC1D23"])


def apresenta_vaga(vaga) -> dict:
    """ Retorna a representação de uma vaga
    """
    return {
        "numero": vaga.numero,
        "status": vaga.status,
        "placa": vaga.placa,
        "hora_entrada": vaga.hora_entrada.isoformat() if vaga.hora_entrada else None,
    }


def apresenta_vagas(vagas: list) -> dict:
    """ Retorna a representação de uma lista de vagas
    """
    return {"vagas": [apresenta_vaga(vaga) for vaga in vagas]}
