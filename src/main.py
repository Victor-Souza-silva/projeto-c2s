from flask import Flask
from flasgger import Swagger
from src.application.controller.vehicle_controller import automovel_bp
from src.application.infrastructure.database_connection import Base, engine

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  
            "model_filter": lambda tag: True,  
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

Swagger(app, config=swagger_config)

app.register_blueprint(automovel_bp)

if __name__ == '__main__':
    app.run(debug=True)
