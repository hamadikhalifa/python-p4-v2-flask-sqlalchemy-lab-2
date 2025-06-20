from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Customer, Item, Review
from sqlalchemy.exc import IntegrityError
from sqlalchemy import event
from sqlalchemy.engine import Engine

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Enable SQLite foreign key enforcement
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Root route
@app.route('/')
def home():
    return {'message': 'Welcome to the API'}, 200

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

# Get a single item by ID
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict()), 200

# Create a new review
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()

    try:
        review = Review(
            comment=data.get('comment'),
            customer_id=data.get('customer_id'),
            item_id=data.get('item_id')
        )
        db.session.add(review)
        db.session.commit()
        return jsonify(review.to_dict()), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid customer_id or item_id'}), 400

# Get all reviews
@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews]), 200

# Delete a review by ID
@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 200

# Update a review's comment
@app.route('/reviews/<int:id>', methods=['PATCH'])
def update_review(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404

    data = request.get_json()
    if 'comment' in data:
        review.comment = data['comment']

    db.session.commit()
    return jsonify(review.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)