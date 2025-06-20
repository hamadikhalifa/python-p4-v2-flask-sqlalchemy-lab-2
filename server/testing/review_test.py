from app import app, db
from models import Customer, Item, Review

class TestReview:
    '''Review model in models.py'''

    def test_can_be_instantiated(self, client):
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self, client):
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self, client):
        with app.app_context():
            assert 'comment' in Review.__table__.columns
            c = Customer(name='Test User')
            i = Item(name='Test Item', price=5.99)
            db.session.add_all([c, i])
            db.session.commit()
            r = Review(comment='great!', customer_id=c.id, item_id=i.id)
            db.session.add(r)
            db.session.commit()
            assert hasattr(r, 'id')
            assert db.session.query(Review).filter_by(id=r.id).first()

    def test_is_related_to_customer_and_item(self, client):
        with app.app_context():
            c = Customer(name='Test User')
            i = Item(name='Test Item', price=5.99)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert r.customer_id == c.id
            assert r.item_id == i.id
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews