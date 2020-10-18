from app import app
from models import User, Card, TradeRequest, RequestCard, db
from unittest import TestCase
from constants import AWS_URL, IMG_FORMAT

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cg_test"

db.drop_all()
db.create_all()

class CardRouteTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.u1 = User.register(username="jcompton", password="qqqqqqqq", first_name="Jon", last_name="Compton", email="j@c.com")
        cls.u2 = User.register(username="klew", password="qqqqqqqq", first_name="Kyle", last_name="Lewis", email="k@l.com")
        db.session.add_all([cls.u1, cls.u2])
        db.session.commit()

        cls.c1 = Card.create(owner_id=cls.u1.id, player="Ken Griffey Jr", year=1989, set_name="Upper Deck", number="1", desc="PSA 10", has_img=True)
        cls.c2 = Card.create(owner_id=cls.u1.id, player="Felix Jose", year=1989, set_name="Upper Deck", number="2", desc="PSA 10")
        db.session.add_all([cls.c1, cls.c2])
        db.session.commit()


    @classmethod
    def tearDownClass(cls):
        db.session.rollback()

    def test_create(self):
        new_card = Card.create(owner_id=self.u1.id, player="Mickey Mantle", year=1952, set_name="Topps", number="311", desc="PSA 2")
        db.session.add(new_card)
        db.session.commit()
        card = Card.query.get(new_card.id)
        self.assertEqual(card.owner_id, self.u1.id)
        self.assertEqual(card.player, new_card.player)
        self.assertEqual(card.set_name, new_card.set_name)
        self.assertEqual(card.number, new_card.number)
        self.assertEqual(card.desc, new_card.desc)
        self.assertFalse(card.has_img)

    def test_serialize(self):
        new_card = Card.create(owner_id=self.u1.id, player="Willie Mays", year=1952, set_name="Topps", number="261", desc="PSA 4")
        db.session.add(new_card)
        db.session.commit()
        card = Card.query.get(new_card.id)
        json = card.serialize()
        self.assertEqual(json.get('player'), new_card.player)
        self.assertEqual(json.get('year'), new_card.year)
        self.assertEqual(json.get('set_name'), new_card.set_name)
        self.assertEqual(json.get('number'), new_card.number)
        self.assertEqual(json.get('description'), new_card.desc)
        self.assertEqual(json.get('title'), new_card.title)
        self.assertEqual(json.get('id'), new_card.id) 

    def test_keys_and_img_urls(self):
        card1 = self.c1
        card2 = self.c2
        self.assertEqual(card1.S3_large_key(), f'cards/{card1.year}/{card1.number}/{card1.id}/large.{IMG_FORMAT}')       
        self.assertEqual(card1.S3_thumb_key(), f'cards/{card1.year}/{card1.number}/{card1.id}/thumb.{IMG_FORMAT}')
        self.assertEqual(card1.img_url(), f'{AWS_URL}cards/{card1.year}/{card1.number}/{card1.id}/large.{IMG_FORMAT}')
        self.assertEqual(card1.thumb_url(), f'{AWS_URL}cards/{card1.year}/{card1.number}/{card1.id}/thumb.{IMG_FORMAT}')
        self.assertIsNone(card2.img_url())

        

