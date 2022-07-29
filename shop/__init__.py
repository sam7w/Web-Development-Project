from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'eea230b690be0c7d8dfac0cbb1f77af763f22f8f296e4859'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1841779:Spyder117@csmysql.cs.cf.ac.uk:3306/c1841779'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes