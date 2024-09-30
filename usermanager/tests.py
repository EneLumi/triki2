from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserManagerTest(TestCase):
    def setUp(self):
        # loo test-kasutaja
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login(self):
        # testi sisselogimise funtsionaalsust
        response = self.client.post(reverse('login'), {'username': 'testuser',
                                                       'password': 'testpass'})  # reverse kontrollib url-i nime järgi (juhuks kui path on muutunud, ja nimi sama)
        self.assertEqual(response.status_code,
                         302)  # eeldab ümbersuunamist (kõik 3-ga algavad teated on seotud ümbersuunamisega)
        self.assertTrue('_auth_user_id' in self.client.session)  # teeb kindlaks kas kasutaja on sisse loginud

    def test_logout(self):
        # logib kastaja sisse
        self.client.login(username='testuser', password='testpass')
        # testib väljalogimist
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # eeldab ümbersuunamist kuna väljalogituna viib uuele lehele
        self.assertFalse('_auth_user_id' in self.client.session)  # kontrollib, et on väljalogitud

    def test_registration(self):
        # testib uue kasutaja loomist
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpass123',  # kontolli, et lahter password1 oleks form-is olemas
            'password2': 'newpass123',  # kontolli, et lahter password2 oleks form-is olemas
            'email': 'newuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        })

        # kui vastus on 302, siis test ok, sest on ümbersuunamine
        self.assertEqual(response.status_code, 302)

        # kontrollib, et kasutaja on loodud
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_home_view(self):
        # kontrollib, et koduleht laeb
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)



