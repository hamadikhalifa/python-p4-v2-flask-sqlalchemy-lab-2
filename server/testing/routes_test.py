from app import app, db
from models import Customer, Item

def test_get_items(client):
    with app.app_context():
        db.session.query(Item).delete()
        db.session.commit()
        item = Item(name='Test Item', price=9.99)
        db.session.add(item)
        db.session.commit()
        item_id = item.id  # Save the ID

    response = client.get('/items')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(i['name'] == 'Test Item' for i in data)

def test_get_item_by_id(client):
    with app.app_context():
        db.session.query(Item).delete()
        db.session.commit()
        item = Item(name='Test Item', price=9.99)
        db.session.add(item)
        db.session.commit()
        item_id = item.id  # Save the ID

    response = client.get(f'/items/{item_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == item_id
    assert data['name'] == 'Test Item'

def test_post_review_success(client):
    with app.app_context():
        db.session.query(Customer).delete()
        db.session.query(Item).delete()
        db.session.commit()
        customer = Customer(name='Test Customer')
        item = Item(name='Test Item', price=9.99)
        db.session.add_all([customer, item])
        db.session.commit()
        customer_id = customer.id
        item_id = item.id

    response = client.post('/reviews', json={
        "comment": "Nice product",
        "customer_id": customer_id,
        "item_id": item_id
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['comment'] == "Nice product"

def test_post_review_invalid_foreign_keys(client):
    with app.app_context():
        db.session.query(Item).delete()
        db.session.commit()
        item = Item(name='Another Item', price=5.99)
        db.session.add(item)
        db.session.commit()
        item_id = item.id

    response = client.post('/reviews', json={
        "comment": "Invalid test",
        "customer_id": 99,  # nonexistent
        "item_id": item_id
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data