from typing import Optional

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
    observacao: Optional[str] = Field(None, description="Observação livre sobre a ocupação da vaga",
                                       examples=["Cliente aguardando revisão do veículo"])
    cpf_cnpj: Optional[str] = Field(
        None, pattern=r"^\d{11}$|^\d{14}$",
        description=("CPF (11 dígitos) ou CNPJ (14 dígitos) do responsável pelo veículo, somente números. "
                      "Quando for um CNPJ, a razão social e os dados de contato da empresa são consultados "
                      "automaticamente; para CPF, nenhuma consulta é realizada."),
        examples=["33555921000170"]
    )


def apresenta_vaga(vaga) -> dict:
    """ Retorna a representação de uma vaga
    """
    return {
        "numero": vaga.numero,
        "status": vaga.status,
        "placa": vaga.placa,
        "hora_entrada": vaga.hora_entrada.isoformat() if vaga.hora_entrada else None,
        "observacao": vaga.observacao,
        "cpf_cnpj": vaga.cpf_cnpj,
        "razao_social": vaga.razao_social,
        "telefone": vaga.telefone,
        "email": vaga.email,
    }


def apresenta_vagas(vagas: list) -> dict:
    """ Retorna a representação de uma lista de vagas
    """
    return {"vagas": [apresenta_vaga(vaga) for vaga in vagas]}
