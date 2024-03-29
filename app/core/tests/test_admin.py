from django.test import TestCase, Client  # import test client to make test requests to our application
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """setup function: a function runs before every test"""
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test_admin@gmail.com",
            password="password123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test_user@gmail.com",
            password="password123",
            name="test user full name"
        )

    def test_users_listed(self):
        """ test that users are listed on users page"""
        url = reverse('admin:core_user_changelist')  # pre-defined url in django
        res = self.client.get(url)
        self.assertContains(res, self.user.name)  # also this implicitly test status is 200
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test that the create user page works """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
