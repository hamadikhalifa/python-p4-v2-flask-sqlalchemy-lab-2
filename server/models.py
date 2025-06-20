from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    reviews = relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    items = association_proxy('reviews', 'item')

    def to_dict(self, include_reviews=True):
        data = {
            "id": self.id,
            "name": self.name,
        }
        if include_reviews:
            # Each review dict omits the customer to avoid recursion
            data["reviews"] = [review.to_dict(include_customer=False) for review in self.reviews]
        return data

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    reviews = relationship('Review', back_populates='item', cascade='all, delete-orphan')

    def to_dict(self, include_reviews=True):
        data = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
        }
        if include_reviews:
            # Each review dict omits the item to avoid recursion
            data["reviews"] = [review.to_dict(include_item=False) for review in self.reviews]
        return data

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, ${self.price:.2f}>"

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)

    customer = relationship('Customer', back_populates='reviews')
    item = relationship('Item', back_populates='reviews')

    def to_dict(self, include_customer=True, include_item=True):
        data = {
            "id": self.id,
            "comment": self.comment,
        }
        if include_customer and self.customer:
            # Omit reviews from customer to avoid recursion
            data["customer"] = self.customer.to_dict(include_reviews=False)
        if include_item and self.item:
            # Omit reviews from item to avoid recursion
            data["item"] = self.item.to_dict(include_reviews=False)
        return data

    def __repr__(self):
        return f"<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>"