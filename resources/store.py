from flask_restful  import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Stores(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be blank')

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'message': 'Store not found'}, 404
        return store.json()

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store already exists.'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Deleted successfully !'}
        return {'message': 'store not found'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
