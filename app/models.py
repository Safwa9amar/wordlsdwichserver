import ast
from marshmallow_sqlalchemy.fields import Nested
from datetime import datetime

# from os.path import join, dirname, realpath
from sqlalchemy import ForeignKey

from flask_login import  UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


# from docx import Document

from datetime import datetime
from app import db,ma



class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    Nom = db.Column(db.String(255),  nullable=False)
    Prenom = db.Column(db.String(255), nullable=False)
    Tel = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    adress = db.Column(db.String(255), unique=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, Nom, email, Prenom, Tel, adress):
        self.username = username
        self.password = generate_password_hash(password)
        self.Nom = Nom
        self.email = email
        self.Prenom = Prenom
        self.Tel = Tel
        self.adress = adress

    def __repr__(self):
        return f'<User {self.username}>'

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Rating(db.Model):
    __tablename__ = 'rating'
    # food data
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    # Custumer id
    UserId = db.Column(db.Integer, ForeignKey("customer.id"))
    user = db.relationship('Customer', backref='rating')

    FoodID = db.Column(db.Integer, ForeignKey("food_category.id"))
    food = db.relationship('Food', backref='__rating')

    def __repr__(self) -> str:
        return '<Rating %r>' % self.id


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    icon_url = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return '<Categories %r>' % self.id


class Supplement(db.Model):
    __tablename__ = 'Supplement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return '<Supplement %r>' % self.id


class ItemSupplement(db.Model):
    __tablename__ = 'item_supplement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    Prix = db.Column(db.Float, nullable=False)
    isAvailable = db.Column(db.Boolean, unique=False, default=True)
    img_url = db.Column(db.String(255), nullable=False)
    max = db.Column(db.Integer, nullable=False)
    # Supplement id
    supplementID = db.Column(db.Integer, ForeignKey("Supplement.id"))
    supplement = db.relationship('Supplement', backref='item_supplement')
    #
    categoryIDs = db.Column(db.String(255), nullable=False)
    # categoryID = db.Column(db.Integer, ForeignKey("categories.id"))
    # category = db.relationship('Categories', backref='item_supplement')

    # categoryIDs = db.relationship("Categories", foreign_keys=[
    #   categoryID], overlaps="category,item_supplement")

    def __repr__(self) -> str:
        return '<Supp %r>' % self.id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.String(255), nullable=False)
    order_date = db.Column(db.DateTime(timezone=True), default=datetime.now)
    DamandeType = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, default=1)

    def __repr__(self) -> str:
        return '<Order %r>' % self.id


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    isViewed = db.Column(db.Boolean, default=False)
    isReaded = db.Column(db.Boolean, default=False)

    # Custumer
    customer_id = db.Column(db.Integer, ForeignKey("customer.id"))
    customer = db.relationship('Customer', backref='notification')
    # order
    order_id = db.Column(db.Integer, ForeignKey("order.id"))
    order = db.relationship('Order', backref='notification')

    def __repr__(self) -> str:
        return '<Notification %r>' % self.id


class Food(db.Model):
    __tablename__ = 'food_category'
    # food data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    Categorie = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    recipes = db.Column(db.String(255), nullable=False)
    with_menu = db.Column(db.Boolean, default=False)
    # category id
    categoryID = db.Column(db.Integer, ForeignKey("categories.id"))
    category = db.relationship('Categories', backref='food_category')
    # ratin
    # ratingID = db.Column(db.Integer, ForeignKey("Rating.id"))
    # rating = db.relationship('Rating', backref='food_category')

    def __repr__(self) -> str:
        return '<Food %r>' % self.id


class Recipe(db.Model):
    __tablename__ = 'recipes'
    # food data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    isCheked = db.Column(db.Boolean, default=True)
    # category id
    FoodID = db.Column(db.Integer, ForeignKey("food_category.id"))
    food = db.relationship('Food', backref='_recipes')

    def __repr__(self) -> str:
        return '<Recip %r>' % self.id


class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        load_instance = True
        include_fk = True
        include_relationships = True


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True
        include_relationships = True


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True
        include_relationships = True


class NotificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True
        include_fk = True
        include_relationships = True


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True
        include_fk = True


class SupplementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Supplement
        load_instance = True
        include_fk = True
        include_relationships = True


class ItemSupplementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemSupplement
        load_instance = True
        # include_fk = True
        # Supplement = Nested(SupplementSchema, many=True)


class FoodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Food
        include_relationships = True
        load_instance = True
        recipes = Nested(RecipeSchema, many=True, exclude=('name',))


class CategoriesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categories
        include_relationships = True
        load_instance = True
        Nested(FoodSchema, many=True)

