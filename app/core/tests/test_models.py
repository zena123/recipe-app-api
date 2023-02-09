from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@gmail.com", password="test"):
    """ create sample user for testing"""
    return get_user_model().objects.create_user(email, password)


# models test
class TestUser(TestCase):
    def test_create_user_with_email_password(self):
        email = "zz@gmail.com"
        password = "Z12345678."
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user)

    def test_new_user_email_normalized(self):
        """ test email of new user created is normalized """
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(email=email)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ test invalid user email"""
        with self.assertRaises(ValueError):
            """anything we run here should raise value error , else test will fail"""
            get_user_model().objects.create_user(None, password="test123")

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser("test@gmail.com", "test123")
        self.assertTrue(user.is_superuser)  # this comes with permissionsMixin
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ test the Tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="test_name"
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """ test the Ingredients string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="ptata"
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """ test the Ingredients string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="shawerma",
            time_minutes=5,
            price=3
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'my_image.jpg')
        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)
