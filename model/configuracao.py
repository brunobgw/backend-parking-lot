from sqlalchemy import Column, Integer, Float

from model import Base


class ConfiguracaoEstacionamento(Base):
    __tablename__ = 'configuracao_estacionamento'

    id = Column("pk_configuracao", Integer, primary_key=True)
    area = Column(Float, nullable=False)
    capacidade = Column(Integer, nullable=False)
    preco_hora = Column(Float, nullable=False)

    def __init__(self, area: float, capacidade: int, preco_hora: float):
        """
        Cria a Configuração do Estacionamento

        Arguments:
            area: área total do estacionamento, em metros quadrados
            capacidade: quantidade máxima de carros que o estacionamento comporta
            preco_hora: valor cobrado por hora de permanência
        """
        self.area = area
        self.capacidade = capacidade
        self.preco_hora = preco_hora
