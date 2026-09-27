from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from typing import Union

from model import Base


class Vaga(Base):
    __tablename__ = 'vaga'

    id = Column("pk_vaga", Integer, primary_key=True)
    numero = Column(Integer, unique=True, nullable=False)
    status = Column(String(10), nullable=False, default="livre")
    placa = Column(String(10), nullable=True)
    hora_entrada = Column(DateTime, nullable=True)
    observacao = Column(String(500), nullable=True)
    cpf_cnpj = Column(String(14), nullable=True)
    razao_social = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

    def __init__(self, numero: int):
        """
        Cria uma Vaga do estacionamento

        Arguments:
            numero: número identificador da vaga
        """
        self.numero = numero
        self.status = "livre"

    def ocupar(self, placa: str, observacao: Union[str, None] = None,
               cpf_cnpj: Union[str, None] = None, razao_social: Union[str, None] = None,
               telefone: Union[str, None] = None, email: Union[str, None] = None,
               hora_entrada: Union[DateTime, None] = None):
        """ Ocupa a vaga com o veículo informado

        Arguments:
            placa: placa do veículo que irá ocupar a vaga
            observacao: observação livre sobre a ocupação da vaga
            cpf_cnpj: CPF ou CNPJ (somente números) do responsável pelo veículo
            razao_social: razão social da empresa, quando o documento é um CNPJ
            telefone: telefone de contato da empresa, quando o documento é um CNPJ
            email: e-mail de contato da empresa, quando o documento é um CNPJ
        """
        self.placa = placa
        self.observacao = observacao
        self.cpf_cnpj = cpf_cnpj
        self.razao_social = razao_social
        self.telefone = telefone
        self.email = email
        self.hora_entrada = hora_entrada or datetime.now()
        self.status = "ocupada"

    def liberar(self):
        """ Libera a vaga, removendo o veículo estacionado
        """
        self.placa = None
        self.observacao = None
        self.cpf_cnpj = None
        self.razao_social = None
        self.telefone = None
        self.email = None
        self.hora_entrada = None
        self.status = "livre"
