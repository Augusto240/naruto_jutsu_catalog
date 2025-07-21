from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Jutsu

class JutsuModelTests(TestCase):
    
    def test_jutsu_creation(self):
        jutsu = Jutsu.objects.create(
            name="Rasengan",
            description="Uma esfera giratória de chakra",
            element_type="wind",
            jutsu_type="offensive",
            rank="A"
        )
        self.assertEqual(jutsu.name, "Rasengan")
        self.assertEqual(jutsu.element_type, "wind")
        self.assertEqual(jutsu.get_element_type_display(), "Vento")
        
    def test_jutsu_str_representation(self):
        jutsu = Jutsu.objects.create(
            name="Chidori",
            description="Concentração de chakra do tipo raio",
            element_type="lightning",
            jutsu_type="offensive",
            rank="A"
        )
        self.assertEqual(str(jutsu), "Chidori (Raio)")

class JutsuViewTests(TestCase):
    
    def setUp(self):
        self.jutsu = Jutsu.objects.create(
            name="Kage Bunshin no Jutsu",
            description="Cria clones físicos do usuário",
            element_type="other",
            jutsu_type="supplementary",
            rank="B"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
    
    def test_jutsu_list_view(self):
        response = self.client.get(reverse('jutsu-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kage Bunshin no Jutsu")
    
    def test_jutsu_detail_view(self):
        response = self.client.get(reverse('jutsu-detail', args=[self.jutsu.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kage Bunshin no Jutsu")
        self.assertContains(response, "Cria clones físicos do usuário")
    
    def test_create_jutsu_requires_login(self):
        response = self.client.get(reverse('jutsu-create'))
        self.assertRedirects(response, f"{reverse('admin:login')}?next={reverse('jutsu-create')}")
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('jutsu-create'))
        self.assertEqual(response.status_code, 200)

class JutsuAPITests(APITestCase):
    
    def setUp(self):
        self.jutsu = Jutsu.objects.create(
            name="Amaterasu",
            description="Chamas negras que queimam por 7 dias",
            element_type="fire",
            jutsu_type="offensive",
            rank="S"
        )

        self.user = User.objects.create_user(
            username='apiuser',
            password='api12345'
        )
    
    def test_get_jutsu_list(self):
        url = reverse('jutsu-list-api')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_jutsu_api(self):
        url = reverse('jutsu-list-api')
        data = {
            'name': 'Tsukuyomi',
            'description': 'Genjutsu poderoso que prende a vítima em uma ilusão',
            'element_type': 'illusion',
            'jutsu_type': 'offensive',
            'rank': 'S'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.login(username='apiuser', password='api12345')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Jutsu.objects.count(), 2)