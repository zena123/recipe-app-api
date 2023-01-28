from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name="main course"):
    """create sample tag"""
    return Tag.objects.create(
        user=user, name=name
    )


def sample_ingredient(user, name="apple"):
    """create sample ingredient"""
    return Ingredient.objects.create(
        user=user,
        name=name)


def sample_recipe(user, **params):
    """ create sample recipe to be used in our tests """
    defaults = {
        'title': 'sample title',
        'time_minutes': 7,
        'price': 55.6
    }
    # use update function on dictionary , it takes a dict then compare
    # it's keys and will update them or create them if they aren't found
    # NOTTE: the ** : it means any extra args will be passed to the params dict and be used later
    defaults.update(params)
    # here ** has opposite effect when calling a function , it will resolve dict and pass it as args
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeAPITests(TestCase):
    """test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ test that authentication is required """
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """test authenticated api access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="test@gmail.com",
            password='12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """test retrieving recipes"""
        sample_recipe(self.user)
        sample_recipe(self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(serializer.data))

    def test_recipes_limited_to_user(self):
        """test retrieving recipes for user """
        user2 = get_user_model().objects.create(
            email='test2@gmail.com',
            password='123456',
        )
        sample_recipe(user2)
        sample_recipe(self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)