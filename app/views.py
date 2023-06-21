from flask import Blueprint


routes = Blueprint('routes', __name__, url_prefix='/api')


@routes.route('/')
def home():
    return {"Hello": "MF"}
