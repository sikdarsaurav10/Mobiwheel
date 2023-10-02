from datetime import datetime
from web import db, login_manager
from flask_login import UserMixin


class People(db.Model):
    id = db.Column('Customer_Id', db.Integer, primary_key=True)
    brand = db.Column('Phone_Brand', db.String(20), nullable=False)
    md = db.Column('Phone_Model', db.String(20), nullable=False)
    name = db.Column('Customer_Name', db.String(50), nullable=False)
    problem = db.Column('Phone_Problem', db.String(100), nullable=True)
    number = db.Column('Contact_Number', db.String(10), nullable=False)


class Phone(db.Model):
    id = db.Column('Customer_Id', db.Integer, primary_key=True)
    public_id = db.Column(db.String(20), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    brand = db.Column('Phone_Brand', db.String(20), nullable=False)
    model = db.Column('Phone_Model', db.String(20), nullable=False)
    ram = db.Column('Ram', db.Integer, nullable=False)
    price = db.Column('Price', db.Integer, nullable=False)
    descp = db.Column('Description', db.Text, nullable=False)
    title_img = db.Column('Title_Image', db.String(20), nullable=False,
                          default='default.jpg')
    photos = db.relationship('Phonephotos', cascade='all,delete',
                             backref='author', lazy=True)


class Phonephotos(db.Model):
    id = db.Column('Customer_Id', db.Integer, primary_key=True)
    phone_img = db.Column(db.String(20), nullable=False)
    phone_id = db.Column(db.String(20), db.ForeignKey('phone.public_id'),
                         nullable=False)


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
