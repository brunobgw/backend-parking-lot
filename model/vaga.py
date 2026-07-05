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

    def __init__(self, numero: int):
        """
        Cria uma Vaga do estacionamento

        Arguments:
            numero: número identificador da vaga
        """
        self.numero = numero
        self.status = "livre"

    def ocupar(self, placa: str, hora_entrada: Union[DateTime, None] = None):
        """ Ocupa a vaga com o veículo informado
        """
        self.placa = placa
        self.hora_entrada = hora_entrada or datetime.now()
        self.status = "ocupada"

    def liberar(self):
        """ Libera a vaga, removendo o veículo estacionado
        """
        self.placa = None
        self.hora_entrada = None
        self.status = "livre"
