from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item should contain a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "Item {} already exits.".format(name)}, 400
        data = Items.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])  # **data
        try:
            item.save_to_db()
        except:
            return {"message": "An Error occurred"}, 500

        return item.json(), 201  # created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {"message": "Item does not exists"}
        item.delete_from_db()
        return {"message": "Item deleted successfully."}

    def put(self, name):
        data = Items.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name,  data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  # [x.json for x in ItemModel.query.all()]
