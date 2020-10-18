from unittest import TestCase
from app import app
from models import User, Card, TradeRequest, RequestCard, db
import json


app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cg_test"
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class TradeRequestTestCase(TestCase):

    def setUp(self):
        TradeRequest.query.delete()
        User.query.delete()
        Card.query.delete()
        RequestCard.query.delete()

    def tearDown(self):
        db.session.rollback()
        

    def test_accept_trade_request(self):
        u3 = User.register(username="dmattingly", password="qqqqqqqq", email="d@m.com", first_name="Wade", last_name="Boggs")
        u4 = User.register(username="dgooden", password="qqqqqqqq", email="d@g.com", first_name="Tony", last_name="Gwynn")
        db.session.add_all([u3, u4])
        db.session.commit()
        c3 = Card.create(owner_id=u3.id, player="Sandy Koufax", year=1955, set_name="Topps", number="123", desc="PSA 7")
        c4 = Card.create(owner_id=u4.id, player="Mickey Mantle", year=1956, set_name="Topps", number="135", desc="PSA 5")
        db.session.add_all([c3, c4])
        db.session.commit()
        u3_id = u3.id
        u4_id = u4.id
        c3_id = c3.id
        c4_id = c4.id
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = u3_id
        tr = TradeRequest(to_id=u3.id, from_id=u4.id)
        db.session.add(tr)
        db.session.commit()
        rc1 = RequestCard(request_id=tr.id, card_id=c3_id, requested=True)
        rc2 = RequestCard(request_id=tr.id, card_id=c4_id)
        db.session.add_all([rc1, rc2])
        tr_id = tr.id
        data = {"accept" : True, "request_id" : f"{tr.id}"}
        res = client.post(f'/users/{u3_id}/requests', data=data)
        req = TradeRequest.query.get(tr_id)
        card3 = Card.query.get(c3_id)
        card4 = Card.query.get(c4_id)    
        self.assertEqual(req.accepted, True)
        self.assertFalse(req.valid_items)
        self.assertEqual(card3.owner_id, u4_id)
        self.assertEqual(card4.owner_id, u3_id)

    def test_decline_trade_request(self):
        user1 = User.register(username="jbagwell", password="qqqqqqqq", email="j@b.com", first_name="Jeff", last_name="Bagwell")
        user2 = User.register(username="djeter", password="qqqqqqqq", email="d@j.com", first_name="Derek", last_name="Jeter")
        db.session.add_all([user1, user2])
        db.session.commit()
        user1_id = user1.id
        user2_id = user2.id
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = user1_id
            new_tr = TradeRequest(from_id=user1_id, to_id=user2_id)
            db.session.add(new_tr)
            db.session.commit()
            data = {"decline" : True, "request_id" : f"{new_tr.id}"}
            res = client.post(f'/users/{user2.id}/requests', data=data)
            req = TradeRequest.query.get(new_tr.id)
            self.assertEqual(req.accepted, False)
            self.assertEqual(req.valid_items, True)

    def test_delete_trade_request(self):
        user1 = User.register(username="jrod", password="qqqqqqqq", email="j@b.com", first_name="Jeff", last_name="Bagwell")
        user2 = User.register(username="ddietrich", password="qqqqqqqq", email="d@j.com", first_name="Derek", last_name="Jeter")
        db.session.add_all([user1, user2])
        db.session.commit()
        user1_id = user1.id
        user2_id = user2.id
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = user1_id
            new_tr = TradeRequest(from_id=user1_id, to_id=user2_id)
            db.session.add(new_tr)
            db.session.commit()
            data = {"delete" : True, "request_id" : f"{new_tr.id}"}
            res = client.post(f'/users/{user2.id}/requests', data=data)
            self.assertEqual(TradeRequest.query.filter_by(id=new_tr.id).first(), None)


    
            