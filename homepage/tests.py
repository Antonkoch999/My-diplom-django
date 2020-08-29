from django.test import TestCase
from django.test import Client
from homepage import models
import ddt
# Create your tests here.


@ddt.ddt
class TestView(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = models.User(first_name='testuser')
        self.user.save()

    @ddt.data(
        '/login/',
        '/logout/',
        '/register/',
        '/profile/',
        '/edit/',
        '/password-change/',
        '/password-change/done/',
        '/registration_confirmation/',
        '/create_profile/',
    )
    def test_url(self, url):
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

#
# class MaterialTestCase(TestCase):
#
#     def setUp(self):
#         super().setUp()
#         self.client = Client()
#         self.user = models.User(first_name='testuser')
#         self.user.save()
#
#     def test_material_created_comment_return_200(self, id_):
#         response = self.client.post('<int:id_>/', {
#             'name': 'test_name',
#             'email': 'test_email',
#             'body': 'testbody',
#         })
#         self.assertEqual(response.status_code, 200)


