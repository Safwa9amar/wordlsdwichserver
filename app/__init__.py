from flask_marshmallow import Marshmallow

# from os.path import join, dirname, realpath
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from flask_jwt_extended import  JWTManager
from datetime import  timedelta


def deleteTabel(tableInstance):
    eng = create_engine('sqlite:///database.db')
    tableInstance.__table__.drop(eng)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'acuUl88CzudhD4ierZDZZeyp5eRmiuz8'
# Change this!
app.config["JWT_SECRET_KEY"] = "mU0acnVXyjYMXkOlcFhJohofJOf7iTXy"
# socketio = SocketIO(app, cors_allowed_origins="*")

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)



from app import routes
