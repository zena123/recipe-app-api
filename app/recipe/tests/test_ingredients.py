from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list') # ingredient not ingredients


class PublicIngredientAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login required to access EP """
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """ test ingredients can be retrieved by authorized users"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@gmail.com",
            password="test123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """test retrieving list of ingredients"""
        Ingredient.objects.create(user=self.user, name="fatoush bread")
        Ingredient.objects.create(user=self.user, name="olive oil")
        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_limited_to_user(self):
        """test returned ingredients only for authenticated user"""
        user2 = get_user_model().objects.create(email='test2@gmail.com', password="i736")
        Ingredient.objects.create(user=user2, name="tomatoes")
        ingredient = Ingredient.objects.create(user=self.user, name='eggs')
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """test creating ingredient object"""
        payload = {'name': 'apple'}
        self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user, name="apple"
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """ test creating invalid ingredient fails"""
        payload = {"name": " "}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_ingredients_assigned_to_recipes(self):
        """test filtering tags by those assigned to recipes"""
        ingredient1 = Ingredient.objects.create(
            user=self.user,
            name="apple",
        )
        ingredient2 = Ingredient.objects.create(
            user=self.user,
            name="chicken",
        )
        recipe = Recipe.objects.create(
            user=self.user,
            title="cake",
            time_minutes=7.0,
            price=4.9,
        )
        recipe.ingredients.add(ingredient1)
        res = self.client.get(INGREDIENT_URL, {'assigned_only':1})
        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_assigned_ingredients_unique(self):
        """test filtering tags assigned to recipes returns unique items"""
        ingredient1 = Ingredient.objects.create(user=self.user, name="apple")
        Ingredient.objects.create(user=self.user, name="banana")
        recipe1= Recipe.objects.create(
            user=self.user,
            title="applePie",
            time_minutes= 3.8,
            price=5.0
        )
        recipe1.ingredients.add()
        recipe2 = Recipe.objects.create(
            user=self.user,
            title="chessee",
            time_minutes=3.8,
            price=6.9
        )
        recipe2.ingredients.add(ingredient1)
        res = self.client.get(INGREDIENT_URL, {'assigned_only':1})
        self.assertEqual(len(res.data), 1)

        

