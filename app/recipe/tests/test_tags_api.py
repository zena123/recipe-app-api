from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITests(TestCase):
    """test public available api for tags"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ test that login required to retrieve tags """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """test the authorized user available apis for tags"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@gmail.com",
            password="password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """test retrieving tasks"""
        Tag.objects.create(user=self.user, name="zozo")
        Tag.objects.create(user=self.user, name="Alabama")
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_tags_limited_to_user(self):
        """test returned tags are only for authenticated user"""
        user2 = get_user_model().objects.create(
            email="test2@gmail.com",
            password="pass12345"
        )
        Tag.objects.create(user=user2, name="test_food")
        tag = Tag.objects.create(user=self.user, name="tooty_frooty")

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """"test creatinh a new tag"""
        payload = {'name': 'test_tag'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user, name="test_tag"
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """"test creating tag with invalid payload"""
        payload = {"name": " "}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


