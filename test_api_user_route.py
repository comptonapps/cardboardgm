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

    def tearDown(self):
        db.session.rollback()
    
    def test_user_api_call(self):
        with app.test_client() as client:
            res = client.get('/api/users')
            json = res.json
            print(json)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json, {'results': [{'email': 't@w.com', 
                                                 'first_name': 'Ted', 
                                                 'id': 1, 
                                                 'img_url': 'https://cardboardgmpics.s3-us-west-2.amazonaws.com/users/profile-img/1/large.JPEG', 
                                                 'last_name': 'Williams', 
                                                 'thumb_url': 'https://cardboardgmpics.s3-us-west-2.amazonaws.com/users/profile-img/1/thumb.JPEG', 
                                                 'username': 'twilliams'}]})



    