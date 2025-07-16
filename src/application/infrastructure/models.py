from sqlalchemy import Column, Integer, String, DECIMAL
from src.application.infrastructure.database_connection import Base

class Automovel(Base):
    __tablename__ = 'automoveis'

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)
    motorizacao = Column(String(20))
    combustivel = Column(String(30))
    cor = Column(String(30))
    quilometragem = Column(Integer)
    numero_portas = Column(Integer)
    transmissao = Column(String(30))
    placa = Column(String(10), unique=True)
    preco = Column(DECIMAL(10, 2))
