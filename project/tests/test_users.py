# project/tests/test_users.py


import json

from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

 
    """
    Test users POST route
    """

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            # message received
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='evan',
                    email='evan@example.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())

            # expected response
            self.assertEqual(response.status_code, 201)
            self.assertIn('evan@example.com was added!', data['message'])
            self.assertIn('success', data['status'])

    
    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is emtpy"""
        with self.client:
            # message received
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())

            # expected response
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])


    def test_add_user_invalid_json_keys(self):
        """Esure error is thrown if the JSON object does not have a username key"""
        with self.client:
            # message received
            response = self.client.post(
                '/users',
                data=json.dumps(dict(email='evan@example.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())

            # expected response
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])



    def test_add_user_duplicate_user(self):
        """Ensure error is thrown if the email already exists"""
        with self.client:
            # message received
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='evan',
                    email='evan@example.com'
                )),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='evan',
                    email='evan@example.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())

            # expected response
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry, that email already exists.', data['message'])
            self.assertIn('fail', data['status'])
