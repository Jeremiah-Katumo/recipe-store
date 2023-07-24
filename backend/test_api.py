import unittest
from main import create_app
from config import TestConfig
from exts import db
import json
from models import User, Recipe
from base64 import b64encode


# Create a class unit test case that inherits from unittest.testcase
class APITestCase(unittest.TestCase):
    # Create a teardown and setup function for declaring different variables to use for our test
    def setUp(self):
        self.app = create_app(TestConfig)

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # create a test client: an interface that flask provides for us to test our application
        # using our test client we can't be apple to make request for our different routes used by our app
        self.client = self.app.test_client(self)

        # You have to be in app context in order to import the db
        # with self.app.app_context():
        #     db.init_app(self.app)

        #     db.create_all()            # It will create a db inside the setup function

    # test the hello route
    def test_hello_world(self):
        hello_response = self.client.get('/recipe/hello')

        status_code = hello_response.status_code

        # json = hello_response.json

        # print(json)
 
        self.assertEqual(status_code, 200)


    def get_auth_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    # test the signup route
    def test_signup(self):
        # add a user
        u = User(username='testuser', email='testuser@test.com', password='password')
        db.session.add(u)
        db.session.commit()

        signup_response = self.client.post(
            '/auth/signup',
            json = {
                "username":"testuser", 
                "email":"testuser@test.com", 
                "password":"password"
            },
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            # headers = self.get_auth_headers('testuser@test.com', 'password')
        )

        status_code = signup_response.status_code

        self.assertEqual(status_code, 200)


    def test_login(self):
        # add a user
        u = User(username='testuser', email='testuser@test.com', password='password')
        db.session.add(u)
        db.session.commit()

        signup_response = self.client.post(
            '/auth/signup',
            json = {
                "username":"testuser", 
                "email":"testuser@test.com", 
                "password":"password"
            },
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            # headers = self.get_auth_headers('testuser@test.com', 'password')
        )
        # status_code = signup_response.status_code

        login_response = self.client.post(
            '/auth/login',
            json = {
            "username":"testuser", 
            "password":"password"
            },
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            # headers = self.get_auth_headers('testuser@test.com', 'password')
        )

        status_code = login_response.status_code

        json = login_response.json

        # print(json)

        self.assertEqual(status_code, 200)


    def test_get_all_recipes(self):
        """TEST GETTING ALL RECIPES"""
        response = self.client.get('/recipe/recipes')

        # print(response.json)

        status_code = response.status_code

        self.assertEqual(status_code, 200)


    def test_get_one_recipe(self):
        id = 1
        response = self.client.get(f'/recipe/recipe/{id}')

        status_code = response.status_code

        self.assertEqual(status_code, 404)


    def get_recipe_headers(self, title, description):
        return {
            'Authorization': 'Basic ' + b64encode(
                (title + ':' + description).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }


    def test_create_recipe(self):

        signup_response = self.client.post(
            '/auth/signup',
            headers = self.get_auth_headers('testuser@test.com', 'password')
        )

        # status_code = signup_response.status_code

        login_response = self.client.post(
            '/auth/login',
            headers = self.get_auth_headers('testuser@test.com', 'password')
        )

        # access_token = login_response.json["access_token"]

        create_recipe_response = self.client.post(
            '/recipe/recipes',
            data = json.dumps(dict(
                title="Test Chapati",
                description="Test Chapati description"
            )),
            # headers = {
            #     # "Authorization": f"Bearer {access_token}",
            #     # 'Accept': 'application/json',
            content_type = 'application/json'
            # }
            # headers = self.get_recipe_headers({'Authorization': f'Bearer {access_token}'})
        )

        data = json.loads(create_recipe_response.data.decode())
        # self.assertTrue(data['title'] == 'Test Chapati')
        # self.assertTrue(data['description'] == 'Test chapati description')
        # self.assertTrue(data['access_token'])
        self.assertTrue(create_recipe_response.content_type == 'application/json')

        status_code = create_recipe_response.status_code

        # print(create_recipe_response.json)
        # json_string = create_recipe_response.content.decode('utf-8')
        # data = json.loads(json_string)
        # json = json.dumps(data)

        self.assertEqual(status_code, 401)


    def test_update_recipe(self):

        signup_response = self.client.post(
            '/auth/signup',
            headers = self.get_auth_headers('testuser@test.com', 'password')
        )

        # status_code = signup_response.status_code

        login_response = self.client.post(
            '/auth/login',
            headers = self.get_auth_headers('testuser@test.com', 'password')
        )

        create_recipe_response = self.client.post(
            '/recipe/recipes',
            headers = self.get_recipe_headers('Test Chapati', 'Test chapati description')
        )
        
        id=1

        update_response = self.client.put(
            f'/recipe/recipe/{id}',
            # json = {
            #     "title":"Test Chapati Updated",
            #     "description":"Test chapati description updated"
            # },
            # headers = {
            #     "Authorization": f"Bearer {access_token}"
            # }
            headers = self.get_recipe_headers('Test Chapati Updated', 'Test chapati description updated')
        )

        # print(update_response.json)

        self.assertEqual(update_response.status_code, 401)


    def test_delete_recipe(self):

        signup_response = self.client.post(
            '/auth/signup',
            headers = self.get_auth_headers('testuser@test.com', 'password')
        )

        # status_code = signup_response.status_code

        login_response = self.client.post(
            '/auth/login',
            headers = self.get_auth_headers('testuser@test.com', 'password')
        )

        create_recipe_response = self.client.post(
            '/recipe/recipes',
            headers = self.get_recipe_headers('Test Chapati', 'Test chapati description')
        )

        id=1

        update_response = self.client.put(
            f'/recipe/recipe/{id}',
            headers = self.get_recipe_headers('Test Chapati Updated', 'Test chapati description updated')
        )

        id=1

        delete_response = self.client.delete(
            f'/recipe/recipe/{id}',
            # headers = {
            #     "Authorization": f"Bearer {access_token}"
            # }
            headers = self.get_recipe_headers('Test Chapati Updated', 'Test chapati description updated')
        )

        # print(delete_response.json)

        self.assertEqual(delete_response.status_code, 401)
        
    # a teardown function for deleting or removing the tables or variables we have
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# specify the test runner: it helps to discover written tests and run the tests
if __name__ == '__main__':
    unittest.main()
