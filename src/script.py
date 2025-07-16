from faker import Faker
from random import choice, randint, uniform
from src.application.infrastructure.database_connection import SessionLocal
from src.application.infrastructure.models import Automovel
from src.application.infrastructure.database_relational import PostgreSQL 

fake = Faker('pt_BR')

marcas_modelos = {
    "Fiat": ["Uno", "Argo", "Mobi", "Cronos"],
    "Chevrolet": ["Onix", "Prisma", "Tracker", "Spin"],
    "Volkswagen": ["Gol", "Polo", "Virtus", "T-Cross"],
    "Toyota": ["Corolla", "Yaris", "Hilux"],
    "Ford": ["Ka", "Fiesta", "EcoSport"]
}

combustiveis = ["Gasolina", "Etanol", "Flex", "Diesel", "Elétrico"]
cores = ["Branco", "Preto", "Prata", "Vermelho", "Cinza", "Azul"]
transmissoes = ["Manual", "Automático", "CVT", "Automatizado"]

def gerar_veiculo_fake():
    marca = choice(list(marcas_modelos.keys()))
    modelo = choice(marcas_modelos[marca])
    return Automovel(
        marca=marca,
        modelo=modelo,
        ano=randint(2010, 2024),
        motorizacao=choice(["1.0", "1.6", "2.0", "2.0 Turbo", "1.4 TSI"]),
        combustivel=choice(combustiveis),
        cor=choice(cores),
        quilometragem=randint(0, 200000),
        numero_portas=choice([2, 3, 4]),
        transmissao=choice(transmissoes),
        placa=fake.license_plate(),
        preco=round(uniform(20000, 180000), 2)
    )

def popular_banco(qtd=100):
    db = PostgreSQL(SessionLocal) 
    for _ in range(qtd):
        veiculo = gerar_veiculo_fake()
        try:
            db.insert_one(veiculo)
        except Exception as e:
            print(f"Erro ao inserir veículo: {e}")
    print(f"{qtd} veículos inseridos com sucesso.")

if __name__ == "__main__":
    popular_banco()
