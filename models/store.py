from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True) # this is our primary key, will start from 1 itself
    name = db.Column(db.String(80), unique=True, nullable=False)

    # this shows that this table is connected with tags and items table
    # we are defining the relationship here
    # lazy=dynamic means that the items here are not going to be fetched from database until we tell it to
    # it is not gonna prefetch them
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
