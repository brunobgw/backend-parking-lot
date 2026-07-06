from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from typing import Union

from model import Base


class Pagamento(Base):
    __tablename__ = 'pagamento'

    id = Column("pk_pagamento", Integer, primary_key=True)
    numero_vaga = Column(Integer, nullable=False)
    placa = Column(String(10), nullable=False)
    valor = Column(Float, nullable=False)
    data_hora = Column(DateTime, nullable=False)

    def __init__(self, numero_vaga: int, placa: str, valor: float,
                 data_hora: Union[DateTime, None] = None):
        """
        Cria um registro de Pagamento recebido

        Arguments:
            numero_vaga: número da vaga relacionada ao pagamento
            placa: placa do veículo relacionado ao pagamento
            valor: valor recebido
            data_hora: data/hora em que o pagamento foi recebido
        """
        self.numero_vaga = numero_vaga
        self.placa = placa
        self.valor = valor
        self.data_hora = data_hora or datetime.now()
