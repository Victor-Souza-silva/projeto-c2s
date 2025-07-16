from flask import Blueprint, request, jsonify, abort
from decimal import Decimal
from src.application.infrastructure.models import Automovel
from src.application.infrastructure.database_connection import SessionLocal
from src.application.infrastructure.database_relational import PostgreSQL
import logging

logging.basicConfig(level=logging.INFO)


automovel_bp = Blueprint("automovel", __name__)
db = PostgreSQL(SessionLocal)

def model_to_dict(obj: Automovel):
    return {
        "id": obj.id,
        "marca": obj.marca,
        "modelo": obj.modelo,
        "ano": obj.ano,
        "motorizacao": obj.motorizacao,
        "combustivel": obj.combustivel,
        "cor": obj.cor,
        "quilometragem": obj.quilometragem,
        "numero_portas": obj.numero_portas,
        "transmissao": obj.transmissao,
        "placa": obj.placa,
        "preco": float(obj.preco) if obj.preco is not None else None
    }

@automovel_bp.route('/automoveis', methods=['GET'])
def listar_automoveis():
    """
    Listar todos os automóveis cadastrados
    ---
    tags:
      - Automóveis
    responses:
      200:
        description: Lista de automóveis
    """
    session = SessionLocal()
    try:
        result = session.query(Automovel).all()
        return jsonify([model_to_dict(row) for row in result])
    finally:
        session.close()

@automovel_bp.route('/automoveis/<int:id>', methods=['GET'])
def buscar_automovel(id):
    """
    Buscar um automóvel pelo ID
    ---
    tags:
      - Automóveis
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do automóvel
    responses:
      200:
        description: Automóvel encontrado
      404:
        description: Automóvel não encontrado
    """
    session = SessionLocal()
    try:
        obj = session.query(Automovel).filter_by(id=id).first()
        if not obj:
            abort(404, description="Automóvel não encontrado")
        return jsonify(model_to_dict(obj))
    finally:
        session.close()

@automovel_bp.route('/automoveis', methods=['POST'])
def criar_automovel():
    """
    Criar um novo automóvel
    ---
    tags:
      - Automóveis
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              marca:
                type: string
                example: "Toyota"
              modelo:
                type: string
                example: "Corolla"
              ano:
                type: integer
                example: 2021
              motorizacao:
                type: string
                example: "2.0"
              combustivel:
                type: string
                example: "Flex"
              cor:
                type: string
                example: "Prata"
              quilometragem:
                type: integer
                example: 30000
              numero_portas:
                type: integer
                example: 4
              transmissao:
                type: string
                example: "Automático"
              placa:
                type: string
                example: "ABC1D23"
              preco:
                type: number
                format: float
                example: 95000.50
    responses:
      201:
        description: Automóvel criado com sucesso
      400:
        description: Erro na criação do automóvel
    """
    data = request.json
    try:
        novo = Automovel(
            marca=data["marca"],
            modelo=data["modelo"],
            ano=data["ano"],
            motorizacao=data.get("motorizacao"),
            combustivel=data.get("combustivel"),
            cor=data.get("cor"),
            quilometragem=data.get("quilometragem"),
            numero_portas=data.get("numero_portas"),
            transmissao=data.get("transmissao"),
            placa=data.get("placa"),
            preco=Decimal(str(data["preco"])) if "preco" in data else None
        )
        db.insert_one(novo)
        return jsonify({"message": "Automóvel criado com sucesso", "id": novo.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@automovel_bp.route('/automoveis/<int:id>', methods=['PUT'])
def atualizar_automovel(id):
    """
    Atualizar um automóvel existente
    ---
    tags:
      - Automóveis
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do automóvel a ser atualizado
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              marca:
                type: string
              modelo:
                type: string
              ano:
                type: integer
              motorizacao:
                type: string
              combustivel:
                type: string
              cor:
                type: string
              quilometragem:
                type: integer
              numero_portas:
                type: integer
              transmissao:
                type: string
              placa:
                type: string
              preco:
                type: number
                format: float
    responses:
      200:
        description: Automóvel atualizado com sucesso
      404:
        description: Automóvel não encontrado
      400:
        description: Erro ao atualizar
    """
    data = request.json
    try:
        atualizado = db.update_one(Automovel, id, data)
        if not atualizado:
            abort(404, description="Automóvel não encontrado")
        return jsonify({"message": "Automóvel atualizado com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@automovel_bp.route('/automoveis/<int:id>', methods=['DELETE'])
def deletar_automovel(id):
    """
    Deletar um automóvel pelo ID
    ---
    tags:
      - Automóveis
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do automóvel
    responses:
      200:
        description: Automóvel deletado com sucesso
      404:
        description: Automóvel não encontrado
    """
    deletado = db.delete_one(Automovel, id)
    if not deletado:
        abort(404, description="Automóvel não encontrado")
    return jsonify({"message": "Automóvel deletado com sucesso"})

@automovel_bp.route('/automoveis/search', methods=['POST'])
def buscar_automoveis_filtro():
    """
    Buscar automóveis com filtros flexíveis
    ---
    tags:
      - Automóveis
    requestBody:
      required: false
      content:
        application/json:
          schema:
            type: object
            properties:
              marca:
                type: string
                example: "Volkswagen"
              modelo:
                type: string
                example: "Gol"
              ano:
                type: integer
                example: 2019
              combustivel:
                type: string
                example: "Flex"
              preco_min:
                type: number
                format: float
                example: 30000
              preco_max:
                type: number
                format: float
                example: 80000
    responses:
      200:
        description: Lista de automóveis filtrados
    """
    filtros = request.json or {}
    logging.info(f"Recebendo filtros de busca: {filtros}")

    session = SessionLocal()
    try:
        query = session.query(Automovel)

        if "marca" in filtros:
            query = query.filter_by(marca=filtros["marca"])
            logging.info(f"Filtrando por marca: {filtros['marca']}")
        if "modelo" in filtros:
            query = query.filter_by(modelo=filtros["modelo"])
            logging.info(f"Filtrando por modelo: {filtros['modelo']}")
        if "ano" in filtros:
            query = query.filter_by(ano=filtros["ano"])
            logging.info(f"Filtrando por ano: {filtros['ano']}")
        if "combustivel" in filtros:
            query = query.filter_by(combustivel=filtros["combustivel"])
            logging.info(f"Filtrando por combustível: {filtros['combustivel']}")
        if "preco_min" in filtros:
            query = query.filter(Automovel.preco >= filtros["preco_min"])
            logging.info(f"Filtrando por preço mínimo: {filtros['preco_min']}")
        if "preco_max" in filtros:
            query = query.filter(Automovel.preco <= filtros["preco_max"])
            logging.info(f"Filtrando por preço máximo: {filtros['preco_max']}")

        results = query.all()
        logging.info(f"{len(results)} resultado(s) encontrado(s).")

        return jsonify([model_to_dict(obj) for obj in results])

    except Exception as e:
        logging.error(f"Erro ao buscar automóveis: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500

    finally:
        session.close()

