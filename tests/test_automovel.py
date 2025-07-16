import pytest
from src.application.infrastructure.models import Automovel
from src.application.infrastructure.database_relational import PostgreSQL
from src.script import gerar_veiculo_fake


@pytest.fixture
def db(test_session):
    return PostgreSQL(test_session)

def test_gerar_veiculo_fake():
    veiculo = gerar_veiculo_fake()
    assert isinstance(veiculo, Automovel)
    assert veiculo.marca is not None
    assert veiculo.modelo is not None
    assert veiculo.ano >= 2010
    assert veiculo.preco > 0

def test_insercao_automovel(db):
    veiculo = gerar_veiculo_fake()
    resultado = db.insert_one(veiculo)
    assert resultado.id is not None
    assert resultado.placa == veiculo.placa

def test_update_automovel(db):
    veiculo = gerar_veiculo_fake()
    inserido = db.insert_one(veiculo)

    atualizado = db.update_one(Automovel, inserido.id, {
        "cor": "Laranja Neon",
        "preco": 99999.99
    })

    assert atualizado.cor == "Laranja Neon"
    assert atualizado.preco == 99999.99

def test_delete_automovel(db):
    veiculo = gerar_veiculo_fake()
    inserido = db.insert_one(veiculo)

    deletado = db.delete_one(Automovel, inserido.id)
    assert deletado.id == inserido.id

    session = db.SessionLocal()
    resultado = session.query(Automovel).filter_by(id=inserido.id).first()
    session.close()
    assert resultado is None
