from app import app
from unittest import TestCase

class AppEntryTestCase(TestCase):

    def test_index(self):
        with app.test_client() as client:
            res = client.get('/index')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("WELCOME TO CARDBOARDGM!", html)

    def test_register(self):
        with app.test_client() as client:
            res = client.get('/register')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("REGISTER", html)
            self.assertIn("Username", html)
            self.assertIn("Password", html)
            self.assertIn("First Name", html)
            self.assertIn("Last Name", html)
            self.assertIn("Email", html)

    def test_login(self):
        with app.test_client() as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Username", html)
            self.assertIn("Password", html)
            self.assertIn("LOGIN", html)
            self.assertIn("LOGIN USER", html)