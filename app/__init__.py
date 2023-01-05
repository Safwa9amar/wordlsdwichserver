from flask_marshmallow import Marshmallow

# from os.path import join, dirname, realpath
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from flask_jwt_extended import  JWTManager
from datetime import  timedelta
# from flask_mail import Mail, Message


# from flask_qrcode import QRcode


def deleteTabel(tableInstance):
    eng = create_engine('sqlite:///site.db')
    tableInstance.__table__.drop(eng)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'acuUl88CzudhD4ierZDZZeyp5eRmiuz8'
# Change this!
app.config["JWT_SECRET_KEY"] = "mU0acnVXyjYMXkOlcFhJohofJOf7iTXy"
# socketio = SocketIO(app, cors_allowed_origins="*")

cors = CORS(app, resources={r"/*": {"origins": "*"}})
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://bsyuwuwa_admin:25.yp3q)4?Mq@localhost/bsyuwuwa_store"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://bsyuwuwa_admin:25.yp3q)4?Mq@worlds-dwich42.com/bsyuwuwa_store"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/bsyuwuwa_store"
# QRcode(app)


db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
    
# app.config['MAIL_SERVER']='mail.worlds-dwich42.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'support@worlds-dwich42.com'
# app.config['MAIL_PASSWORD'] = 'astro0674020244'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = False
# mail = Mail(app)

# @app.route('/sendmail', methods=["GET", "POST"])
# def send_mail():
#     msg = Message('Hello from the other side!',
#                   sender='support@worlds-dwich42.com', recipients=['hassanih97@gmail.com'])
#     msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
#     print(msg)
#     mail.connect()
#     mail.send(msg)
#     return "Message sent!"


from app import routes
