from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Items, ItemList
from resources.store import Stores, StoreList
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flaskRest'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'pratisha'
# app.config['JWT_AUTH_URL_RULE'] = '/login'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

api = Api(app)


jwt = JWT(app, authenticate, identity)  #/auth

api.add_resource(Stores, '/store/<string:name>')
api.add_resource(Items, '/item/<string:name>') # same as @app.route('/item/<string: name>') http://127.0.0.1:5000/item/chair
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':          # it prevents app from running when app is imported in any file
    db.init_app(app)
    app.run(port=5000, debug=True)
