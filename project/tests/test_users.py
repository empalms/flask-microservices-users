# project/tests/test_users.py


import json
import datetime

from project import db
from project.tests.base import BaseTestCase
from project.api.models import User


# helper functions 

def add_user(username, email, created_at=datetime.datetime.utcnow()):
    """Helper for adding users to database"""
    user = User(username=username, email=email, created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user



# tests

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
    Test main route - DEPRECATED
    """

    # def test_main_no_users(self):
    #     """
    #     Ensure the main route behaves correctly when 
    #     no users have been added to the database.
    #     """
    #     # request received
    #     response = self.client.get('/')
    #     # expected response
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'<h1>All Users</h1>', response.data)
    #     self.assertIn(b'<p>No users!</p>', response.data)


    # def test_main_with_users(self):
    #     """
    #     Ensure the main route behaves correctly when users have been
    #     added to the database.
    #     """
    #     # db state
    #     add_user('evan', 'evan@example.com')
    #     add_user('palmer', 'palmer@example.com')
    #     # request received
    #     response = self.client.get('/')
    #     # expected response
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'<h1>All Users</h1>', response.data)
    #     self.assertNotIn(b'<p>No users!</p>', response.data)
    #     self.assertIn(b'<strong>evan</strong>', response.data)
    #     self.assertIn(b'<strong>palmer</strong>', response.data)
 
    
    # def test_main_add_user(self):
    #     """Ensure a new user can be added to the database."""
    #     with self.client:
    #         # request received
    #         response = self.client.post(
    #             '/',
    #             data=dict(username='evan', email='evan@example.com'),
    #             follow_redirects=True
    #         )
    #         # expected response
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'<h1>All Users</h1>', response.data)
    #         self.assertNotIn(b'<p>No users!</p>', response.data)
    #         self.assertIn(b'<strong>evan</strong>', response.data)




    """
    Test users POST route
    """

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            # request received
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
            # request received
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            # expected response
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])


    def test_add_user_invalid_json_keys(self):
        """Esure error is thrown if the JSON object does not have a username key"""
        with self.client:
            # request received
            response = self.client.post(
                '/users',
                data=json.dumps(dict(email='evan@example.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            # expected response
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])



    def test_add_user_duplicate_user(self):
        """Ensure error is thrown if the email already exists"""
        with self.client:
            # db state
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='evan',
                    email='evan@example.com'
                )),
                content_type='application/json',
            )
            # request received 
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
            self.assertIn('Sorry, that email already exists', data['message'])
            self.assertIn('fail', data['status'])



    """
    GET single user
    """

    def test_single_user(self):
        """Ensure get single user behaves correctly"""
        # db state
        user =  add_user(username='evan', email='evan@example.com')
        with self.client:
            # request recieved
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            # expected response
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('evan', data['data']['username'])
            self.assertIn('evan@example.com', data['data']['email'])
            self.assertIn('success', data['status'])


    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            # request received
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            # expected response
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])


    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            # request received
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            #expected response
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])


    """
    GET all users
    """

    def test_all_users(self):
        """Ensure get all users behaves correctly"""
        # db state
        created = datetime.datetime.utcnow() + datetime.timedelta(-30)
        add_user('evan', 'evan@example.com', created)
        add_user('palmer', 'palmer@example.com')
        with self.client:
            # request received
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            # response expected
            self.assertEqual(response.status_code, 200)
            # ensure 2 users
            self.assertEqual(len(data['data']['users']), 2)
            # ensure created_at is not null
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            # 1st user
            self.assertIn('evan', data['data']['users'][1]['username'])
            self.assertIn('evan@example.com', data['data']['users'][1]['email'])
            # 2nd user
            self.assertIn('palmer', data['data']['users'][0]['username'])
            self.assertIn('palmer@example.com', data['data']['users'][0]['email'])
            # response message
            self.assertIn('success', data['status'])
