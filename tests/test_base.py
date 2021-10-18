from flask_testing import TestCase
from flask import current_app, url_for

from main import app

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        return app

    #prueba: validacion que existe la app
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    #prueba: validacion en modo test
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    #prueba de redireccion
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response,url_for('hello') )

    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)

    def test_hello_post(self):
        #fake_form ={
        #    'username':'fake',
        #    'password':'fake-pass'
        #}
        reponse = self.client.post(url_for('hello'))
        self.assertTrue(reponse.status_code, 405)

    def test_auth_blueprint_exists(self):
        self.assertIn('auth',self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_auth_login_template(self): 
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fake_form =  {
            'username':'fake',
            'password': 'fake-password'
        }

        reponse = self.client.post(url_for('auth.login'),data=fake_form)
        self.assertRedirects(reponse, url_for('index'))
        


    

    