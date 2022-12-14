import ast
from marshmallow_sqlalchemy.fields import Nested
from datetime import datetime

# from os.path import join, dirname, realpath
from sqlalchemy import ForeignKey

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


# from docx import Document

from datetime import datetime
from app import db, ma


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    Nom = db.Column(db.String(80),  nullable=False)
    Prenom = db.Column(db.String(80), nullable=False)
    Tel = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    # ADRESS AND INFORMATIONS

    adress_exct = db.Column(db.String(255), nullable=False)
    batiment = db.Column(db.String(255), nullable=False)
    etage = db.Column(db.Integer, nullable=False)
    sonnerie = db.Column(db.Boolean, default=False)
    code = db.Column(db.Integer, nullable=False)

    # adress  Quartier
    adress = db.Column(db.Integer, ForeignKey("Livraison_adresses.id"))

    def __init__(self, username, password, Nom, email, Prenom, Tel, adress, adress_exct,
                 batiment,
                 etage,
                 sonnerie,
                 code):
        self.username = username
        self.password = generate_password_hash(password)
        self.Nom = Nom
        self.email = email
        self.Prenom = Prenom
        self.Tel = Tel
        self.adress = adress
        self.adress_exct = adress_exct
        self.batiment = batiment
        self.etage = etage
        self.sonnerie = sonnerie
        self.code = code

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
    avatar = db.Column(db.String(2500), nullable=False)

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
    cutting_off = db.Column(db.Float, nullable=False)
    cutting_off_status = db.Column(db.Boolean, nullable=False, default=False)

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
    Note = db.Column(db.String(255), nullable=False)

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
    etat = db.Column(db.Boolean, default=False)
    # with_options = db.Column(db.Boolean, default=False)
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


class CommandType(db.Model):
    __tablename__ = 'command_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    isCheked = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return '<Command %r>' % self.id


class FraisDeLivraison(db.Model):
    __tablename__ = 'livraison_frais'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return '<Frais %r>' % self.id


class LivraisonAdress(db.Model):
    __tablename__ = 'Livraison_adresses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    frais_price = db.Column(db.Float, nullable=False)
    isActived = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return '<Adress %r>' % self.id


class WorkHours(db.Model):
    __tablename__ = 'work_hours'
    id = db.Column(db.Integer, primary_key=True)
    dayName = db.Column(db.String(200), nullable=False)
    from_hour = db.Column(db.Time, nullable=False)
    to_hour = db.Column(db.Time, nullable=False)

    def __repr__(self) -> str:
        return '<WorkHours %r>' % self.id


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    tel1 = db.Column(db.String(200), nullable=False)
    tel2 = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), nullable=False)
    facebook = db.Column(db.String(200), nullable=False)
    instagram = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return '<Contact %r>' % self.id


class notificationSound(db.Model):
    __tablename__ = 'notification_sound'
    id = db.Column(db.Integer, primary_key=True)
    isActivated = db.Column(db.Boolean, nullable=False)

    def __repr__(self) -> str:
        return '<Notification_sound %r>' % self.id


class clientStatus(db.Model):
    __tablename__ = 'client_status'
    id = db.Column(db.Integer, primary_key=True)
    isActivated = db.Column(db.Boolean, nullable=False)

    def __repr__(self) -> str:
        return '<client_status %r>' % self.id


class GlobalPromotion(db.Model):
    __tablename__ = 'global_promotion'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return '<global_promotion %r>' % self.id


class Promotion(db.Model):
    __tablename__ = 'promotion'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    promotionGlobal = db.Column(db.Float, nullable=False, default=0)

    # relation for category
    categoryID = db.Column(db.Integer, ForeignKey("categories.id"))
    cutting_off = db.Column(db.Float, nullable=False)
    cutting_off_status = db.Column(db.Boolean, nullable=False, default=False)
    # relation for order
    orderID = db.Column(db.Integer, ForeignKey("order.id"))

    def __repr__(self) -> str:
        return '<Promotion %r>' % self.id


class TableReservation(db.Model):
    __tablename__ = 'table_reservation'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nom = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    person_count = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return '<Table %r>' % self.id

# generate CommandTypeSchema for CommandType class


class TableReservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Promotion
        load_instance = True
        include_fk = True


class PromotionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Promotion
        load_instance = True
        include_fk = True
        include_relationships = True


class GlobalPromotionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GlobalPromotion
        load_instance = True
        include_fk = True


class clientStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = clientStatus
        load_instance = True
        include_fk = True


class notificationSoundSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = notificationSound
        load_instance = True
        include_fk = True


class ContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        load_instance = True
        include_fk = True


class WorkHoursSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkHours
        load_instance = True
        include_fk = True


class LivraisonAdressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LivraisonAdress
        load_instance = True
        include_fk = True


class FraisDeLivraisonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FraisDeLivraison
        load_instance = True
        include_fk = True


class CommandTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CommandType
        load_instance = True
        include_fk = True


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
