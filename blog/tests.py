from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class SetUp:
    pass


class BlogTests(TestCase):
    fixtures = ["fixture.json"]

    def setUp(self):
        """
        Customer User Login Data
        """
        # Defining URl
        self.data = SetUp

    def test_get_my_edited_articles_without_authorization(self):
        client = APIClient()
        r = client.get(reverse("blog-api-v1:ArticleEdited"), format="multipart")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_my_edited_articles_without_authorization(self):
        client = APIClient()
        r = client.get(reverse("blog-api-v1:ArticleEdited"), format="multipart")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_artical_approval_without_authorization(self):
        client = APIClient()
        r = client.get(reverse("blog-api-v1:ArticleApproval"))
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
