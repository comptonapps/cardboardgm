from app import app
from models import User, Card, TradeRequest, RequestCard, db
from unittest import TestCase
from constants import AWS_URL, IMG_FORMAT

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cg_test"
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class UserRouteTestCase(TestCase):

    def setUp(self):
        User.query.delete()
        

    def tearDown(self):
        db.session.rollback()

    def test_users(self):
        u1 = User.register(username="mgonzales", password="qqqqqqqq", email="m@g.com", first_name="Marco", last_name="Gonzales")
        u2 = User.register(username="mmcgwire", password="qqqqqqqq", email="m@m.com", first_name="Mark", last_name="McGwire")
        db.session.add_all([u1, u2])
        db.session.commit()
        user1 = User.query.get(u1.id)
        user2 = User.query.get(u2.id)
        user1_id = user1.id
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = user1_id
            res = client.get('/users', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertIn(user2.username, html)
            self.assertIn(user1.username, html)
            self.assertIn("All Managers", html)

    def test_user_by_id(self):
        u1 = User.register(username="mgonzales", password="qqqqqqqq", email="m@g.com", first_name="Marco", last_name="Gonzales")
        u2 = User.register(username="mmcgwire", password="qqqqqqqq", email="m@m.com", first_name="Mark", last_name="McGwire")
        db.session.add_all([u1, u2])
        db.session.commit()
        user1 = User.query.get(u1.id)
        user2 = User.query.get(u2.id)
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = user1.id
            res = client.get(f'users/{user1.id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Edit Profile', html)
            self.assertIn(user1.username, html)
            self.assertIn("Add to Collection", html)

    def test_user_delete(self):
        u1 = User.register(username="mgonzales", password="qqqqqqqq", email="m@g.com", first_name="Marco", last_name="Gonzales")
        db.session.add(u1)
        db.session.commit()
        user1 = User.query.get(u1.id)
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['user_id'] = user1.id
            res = client.post(f'users/{user1.id}/delete')
            self.assertEqual(res.status_code, 302)
            self.assertIsNone(User.query.filter_by(id=user1.id).first())
