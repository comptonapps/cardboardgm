from app import app
from models import User, Card, TradeRequest, RequestCard, db
from unittest import TestCase
from constants import AWS_URL, IMG_FORMAT

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cg_test"
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class UserApiCallTestCase(TestCase):

    def setUp(self):
        User.query.delete()
        new_user = User.register(username="twilliams", password="qqqqqqqq", email="t@w.com", first_name="Ted", last_name="Williams")
        db.session.add(new_user)
        db.session.commit()

        self.user_id = new_user.id

        Card.query.delete()
        new_card = Card.create(owner_id = self.user_id, player="Mickey Mantle", year=1952, set_name="Topps", number="311", desc="PSA 2")
        db.session.add(new_card)
        db.session.commit()

        self.user_id = new_user.id
        self.card_id = new_card.id

    def tearDown(self):
        db.session.rollback()
    
    def test_card_api_call(self):
        with app.test_client() as client:
            res = client.get('/api/cards')
            json = res.json
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json, {'results': [{'description': 'PSA 2', 
                                    'full_url' : None, 
                                    'id'       : 1, 
                                    'number'   : '311', 
                                    'player'   : 'Mickey Mantle', 
                                    'set_name' : 'Topps', 
                                    'thumb_url': None, 
                                    'title'    : '1952 Topps #311 Mickey Mantle PSA 2', 
                                    'year'     : 1952}]})
        