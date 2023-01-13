from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


# route means the route through which we will get the request
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    # respone-  this is whatever we return, 200 is the respone code and we return itemschema object
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):  # we are getting item_id from the user
        # this is like filtering the item_id and checking if it is correct and then returning the object of it
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilige required")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    # arguments means that what type of data we will be getting as json from the user
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    # respone-  this is whatever we return, 200 is the respone code and we return itemschema object
    @blp.response(200, ItemSchema)  # reponce should be deeper than arguments
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # this means that we need to login and need access token
    @jwt_required(fresh=True)
    # arguments means that what type of data we will be getting as json from the user
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
