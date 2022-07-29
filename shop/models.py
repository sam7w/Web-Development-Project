
from datetime import datetime
from shop import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(20),nullable=False)
    watches = db.relationship('Watch', backref='brand', lazy=True)

    def __repr__(self):
        return f"Brand('{self.brand_name}')"

class Watch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    quick_description = db.Column(db.String(200), nullable=False)
    water_resistance = db.Column(db.String(100), nullable=False)
    braclet  = db.Column(db.String(200), nullable=False)
    movement = db.Column(db.String(200), nullable=False)
    bezel = db.Column(db.String(400), nullable=False)
    watch_size = db.Column(db.Numeric(2), nullable = False)
    #publication_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Numeric(10,2), nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    stock_level = db.Column(db.Integer, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)

    def __repr__(self):
        return f"Watch('{self.title}', '{self.description}', '{self.price}', '{self.stock_level}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20),unique=False, nullable=False)
    last_name = db.Column(db.String(20),unique=False, nullable=False)
    address = db.Column(db.String(120),unique=False, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}','{self.username}','{self.address}','{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
