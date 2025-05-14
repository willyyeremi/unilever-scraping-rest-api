from flask import Flask
from routes import data


app = Flask(__name__)
app.register_blueprint(data)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5001, debug = True)