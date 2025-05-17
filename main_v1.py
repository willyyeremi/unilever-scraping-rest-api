from flask import Flask
from flask_jwt_extended import JWTManager

from routes import data_bp
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(data_bp)

jwt = JWTManager()
jwt.init_app(app)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5011, debug = True)