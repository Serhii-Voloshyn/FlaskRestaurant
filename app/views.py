from flask import Blueprint, request, current_app
from pydantic.error_wrappers import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from sqlalchemy.sql import func

from app.models import db, User, Restaurant, Employee, Menu, MenuItem, Vote
import app.schemas as schema
from app.utils import token_required


routes = Blueprint("routes", __name__, url_prefix="/api")


@routes.route("/user_create", methods=["POST"])
def user_create():
    try:
        user = schema.User(**dict(request.json))
        user.password = generate_password_hash(user.password)
    except ValidationError as e:
        return e.json(), 400

    if User.query.filter_by(username=user.username).all():
        return "Username exists", 400

    if User.query.filter_by(email=user.email).all():
        return "Email exists", 400

    user = User(**user.__dict__)
    db.session.add(user)
    db.session.commit()

    return user.serialize, 201


@routes.route("/login", methods=["POST"])
def login():
    try:
        auth = schema.Login(**dict(request.json))
    except ValidationError as e:
        return e.json(), 400

    user = User.query\
        .filter_by(username=auth.username)\
        .first()

    if not user:
        # returns 401 if user does not exist
        return "User doesn't exist", 400

    if not check_password_hash(user.password, auth.password):
        return "Wrong username or password", 400

    token = jwt.encode({
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }, current_app.config["SECRET_KEY"])

    return {"token": token}, 200


@routes.route("/restaurant_create", methods=["POST"])
@token_required
def restaurant_create(current_user):
    try:
        restaurant = schema.Restaurant(**dict(request.json))
    except ValidationError as e:
        return e.json(), 400

    try:
        restaurant = Restaurant(**restaurant.__dict__)
        db.session.add(restaurant)
        db.session.commit()
    except Exception as e:
        return {"DB WENT NUTS": e}, 400

    return restaurant.serialize, 201


@routes.route("/employee_create", methods=["POST"])
@token_required
def employee_create(current_user):
    try:
        employee = schema.Employee(**dict(request.json))
    except ValidationError as e:
        return e.json(), 400

    try:
        employee = Employee(**employee.__dict__)
        db.session.add(employee)
        db.session.commit()
    except Exception as e:
        return {"DB WENT NUTS": e}, 400

    return employee.serialize, 201


@routes.route("/menu_create", methods=["POST"])
@token_required
def menu_create(current_user):
    try:
        menu = schema.Menu(**dict(request.json))
    except ValidationError as e:
        return e.json(), 400

    restaurant = Restaurant.query.filter_by(id=menu.restaurant_id).first()
    if not restaurant:
        return "Restaurant doesn't exist", 400

    try:
        menu = Menu(**menu.__dict__)
        db.session.add(menu)
        db.session.commit()
    except Exception as e:
        return {"DB WENT NUTS": e}, 400

    return menu.serialize, 201


@routes.route("/menu_get_all", methods=["GET"])
def menu_get_all():
    menus = Menu.query.all()
    menus = [menu.serialize for menu in menus]
    return menus, 200


@routes.route("/menu_get/<day>", methods=["GET"])
def get_by_day(day):
    menus = Menu.query.filter_by(day=day).all()
    menus = [menu.serialize for menu in menus]

    for menu in menus:
        menu["items"] = [
            item.serialize
            for item in MenuItem.query.filter_by(menu_id=menu["id"]).all()
        ]

    return menus, 200


@routes.route("/item_create", methods=["POST"])
@token_required
def item_create(current_user):

    try:
        menu_item = schema.MenuItem(**dict(request.json))
    except ValidationError as e:
        return e.json(), 400

    menu = Menu.query.filter_by(id=menu_item.menu_id).all()

    if not menu:
        return "Menu doesn't exist", 400

    try:
        menu_item = MenuItem(**menu_item.__dict__)
        db.session.add(menu_item)
        db.session.commit()
    except Exception as e:
        return {"DB WENT NUTS": e}, 400

    return menu_item.serialize, 201


@routes.route("/vote", methods=["POST"])
@token_required
def create_vote(current_user):
    try:
        vote = schema.Vote(**dict(request.json))
    except ValidationError as e:
        return e.json(), 400

    menu = Menu.query.filter_by(id=vote.menu_id).all()

    if not menu:
        return "Menu doesn't exist", 400

    employee = Employee.query.filter_by(id=vote.employee_id).all()

    if not employee:
        return "Employee doesn't exist", 400

    employee_votes = Vote.query.filter_by(
        employee_id=vote.employee_id, menu_id=vote.menu_id
        ).all()

    if employee_votes:
        return "Employee has already voted for this menu", 400

    try:
        vote = Vote(**vote.__dict__)
        db.session.add(vote)
        db.session.commit()
    except Exception as e:
        return {"DB WENT NUTS": e}, 400

    return vote.serialize, 20


@routes.route("/vote_get/<menu_id>", methods=["GET"])
def get_vote_by_menu(menu_id):

    menu = Menu.query.filter_by(id=menu_id).all()

    if not menu:
        return "Menu doesn't exist", 400

    votes = Vote.query.filter_by(menu_id=menu_id).all()
    avg = db.session.query(
        func.avg(Vote.score)
    ).filter_by(menu_id=menu_id).one()

    votes = [vote.serialize for vote in votes]
    return {"message": "Successfully retreived", "vote": votes, "avg": avg[0]}
