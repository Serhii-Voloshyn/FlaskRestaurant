from flask_sqlalchemy import SQLAlchemy

import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    full_name = db.Column(db.String(80), nullable=True, default="Anonimous")
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    disabled = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
        user = dict(
            id=self.id,
            username=self.username,
            full_name=self.full_name,
            email=self.email,
            password=self.password,
            disabled=self.disabled,
        )
        return user


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=False)

    @property
    def serialize(self):
        restaurant = dict(
            id=self.id,
            full_name=self.full_name,
            email=self.email
        )
        return restaurant


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)

    @property
    def serialize(self):
        restaurant = dict(
            id=self.id,
            name=self.name
        )
        return restaurant


class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurant.id))
    day = db.Column(db.Date, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        menu = dict(
            id=self.id,
            restaurant_id=self.restaurant_id,
            day=self.day
        )

        return menu


class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_id = db.Column(db.Integer, db.ForeignKey(Menu.id))
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(2), nullable=False)

    @property
    def serialize(self):
        item = dict(
            id=self.id,
            menu_id=self.menu_id,
            name=self.name,
            price=self.price
        )
        return item


class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey(Employee.id))
    menu_id = db.Column(db.Integer, db.ForeignKey(Menu.id))
    score = db.Column(db.Integer)

    @property
    def serialize(self):
        vote = dict(
            id=self.id,
            employee_id=self.employee_id,
            menu_id=self.menu_id,
            score=self.score
        )
        return vote
