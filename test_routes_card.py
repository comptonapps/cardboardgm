from app import app
from models import User, Card, TradeRequest, RequestCard, db
from unittest import TestCase
from constants import AWS_URL, IMG_FORMAT

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cg_test"
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class CardsRouteTestCase(TestCase):

    def setUp(self):
        User.query.delete()
        Card.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_cards_route(self):
        u1 = User.register(username="ddiggler", password="qqqqqqqq", first_name="Jon", last_name="Compton", email="j@c.com")
        u2 = User.register(username="scottyj", password="qqqqqqqq", first_name="Kyle", last_name="Lewis", email="k@l.com")
        db.session.add_all([u1, u2])
        db.session.commit()
        c1 = Card.create(owner_id=u1.id, player="Ken Griffey Jr", year=1989, set_name="Upper Deck", number="1", desc="PSA 10", has_img=True)
        c2 = Card.create(owner_id=u2.id, player="Felix Jose", year=1989, set_name="Upper Deck", number="2", desc="PSA 10")
        db.session.add_all([c1, c2])
        db.session.commit()
        with app.test_client() as client:
            res = client.get('/cards')
            html = res.get_data(as_text=True)
            self.assertIn("Griffey", html)
            self.assertIn("Felix", html)
            self.assertIn("All Cards", html)

   
    

    def test_card_id_route(self):
        u1 = User.register(username="ddiggler", password="qqqqqqqq", first_name="Jon", last_name="Compton", email="j@c.com")
        db.session.add(u1)
        db.session.commit()
        c1 = Card.create(owner_id=u1.id, player="Ken Griffey Jr", year=1989, set_name="Upper Deck", number="1", desc="PSA 10", has_img=True)
        c2 = Card.create(owner_id=u1.id, player="Felix Jose", year=1989, set_name="Upper Deck", number="2", desc="PSA 10")
        db.session.add_all([c1, c2])
        db.session.commit()
        with app.test_client() as client:
            res = client.get(f'/cards/{c1.id}')
            html = res.get_data(as_text=True)
            user1 = User.query.get(u1.id)
            self.assertIn("Griffey", html)
            self.assertIn(f"{user1.username}", html)
            self.assertNotIn("Felix", html)

    def test_card_delete(self):
        u1 = User.register(username="ddiggler", password="qqqqqqqq", first_name="Jon", last_name="Compton", email="j@c.com")
        db.session.add(u1)
        db.session.commit()
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id']= u1.id
            card = Card.create(owner_id=u1.id, player="Fernando Tatis Jr", year=2019, set_name="Topps Series 2", number="410", desc="PSA 10")
            db.session.add(card)
            db.session.commit()
            client.post(f'/cards/{card.id}/delete')
            res = client.get(f'/cards/{card.id}')
            self.assertEqual(res.status_code, 404)

    def test_card_edit(self):
        u1 = User.register(username="ddiggler", password="qqqqqqqq", first_name="Jon", last_name="Compton", email="j@c.com")
        db.session.add(u1)
        db.session.commit()
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = u1.id
        card = Card.create(owner_id=u1.id, player="Fernando Tatis Jr", year=2019, set_name="Topps Series 2", number="410", desc="PSA 10")
        db.session.add(card)
        db.session.commit()
        data = {'player' : 'Ronald Acuna Jr', 'year' : 2018, 'set_name' : "topps Series 2", "number" : "698", "desc" : "Short Print"}
        res = client.post(f'/cards/{card.id}/edit', data=data)
        self.assertEqual(card.player, data['player'])
        self.assertEqual(card.year, data['year'])
        self.assertEqual(card.number, data['number'])
        self.assertEqual(card.desc, data['desc'])
