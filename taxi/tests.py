from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

TestCase.fixtures = ["taxi_service_db_data.json"]


class PublicTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertRedirects(response, "/login/?next=/cars/", status_code=302)

    def test_index_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateHomeTests(TestCase):
    def setUp(self) -> None:
        self.client.force_login(get_user_model().objects.get(id=1))

    def test_index(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_visit_counter(self):
        visits = 3
        for visit in range(visits):
            response = self.client.get(reverse("taxi:index"))
            self.assertEqual(response.context["num_visits"], visit + 1)
