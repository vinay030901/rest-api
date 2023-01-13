from db import db


class ItemModel(db.Model):  # it is inheriting from db.Model
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String())
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    # the value in store_id will have to match a value in store table id, that's why it is the foreign key for us
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="items")

    # it will fill the data in secondary table
    tags = db.relationship(
        "TagModel", back_populates="items", secondary="items_tags")
