from unittest import TestCase
from app import app
from models import User, Card, TradeRequest, RequestCard, db
import json


app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cg_test"
app.config['WTF_CSRF_ENABLED'] = False


class TradeRequestTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()

    def setUp(self):
        TradeRequest.query.delete()
        User.query.delete()
        Card.query.delete()
        RequestCard.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_create_trade_request(self):
        u1 = User.register(username="wboggs", password="qqqqqqqq", email="w@b.com", first_name="Wade", last_name="Boggs")
        u2 = User.register(username="tgwynn", password="qqqqqqqq", email="t@g.com", first_name="Tony", last_name="Gwynn")
        db.session.add_all([u1, u2])
        db.session.commit()

        c1 = Card.create(owner_id=u1.id, player="Sandy Koufax", year=1955, set_name="Topps", number="123", desc="PSA 7")
        c2 = Card.create(owner_id=u2.id, player="Mickey Mantle", year=1956, set_name="Topps", number="135", desc="PSA 5")
        db.session.add_all([c1, c2])
        db.session.commit()
        jsn = json.dumps({"c" : [str(c1.id)]})
        data = {'req_data' : jsn}
        c2_id = c2.id
        c1_id = c1.id
        u1_id = u1.id
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = u1_id
            res = client.post(f'/cards/{c2_id}/new-request', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            card1 = Card.query.get(c1_id)
            card2 = Card.query.get(c2_id)
            trade_requests = TradeRequest.query.all()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(trade_requests), 1)
            self.assertEqual(trade_requests[0].to_id, 2)
            self.assertEqual(trade_requests[0].from_id, 1)
            self.assertIn(card1, trade_requests[0].cards)
            self.assertIn(card2, trade_requests[0].cards)



