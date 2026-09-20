from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Category, Item, Profile


class ModelTestCase(TestCase):
    """Tests for database models and signal handlers."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.item = Item.objects.create(
            category=self.category,
            seller=self.user,
            title='Test Laptop',
            description='A test laptop description',
            price=499.99
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Electronics')
        self.assertEqual(self.category.slug, 'electronics')

    def test_item_creation(self):
        self.assertEqual(str(self.item), 'Test Laptop')
        self.assertEqual(self.item.price, 499.99)
        self.assertFalse(self.item.is_sold)
        self.assertEqual(self.item.seller, self.user)

    def test_profile_auto_creation_signal(self):
        """Verify that creating a User automatically creates an associated Profile via signals."""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = self.user.profile
        self.assertEqual(str(profile), "testuser's Profile")


class ViewTestCase(TestCase):
    """Tests for HTTP views and authentication protection."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='seller', password='password123')
        self.category = Category.objects.create(name='Books', slug='books')
        self.item = Item.objects.create(
            category=self.category,
            seller=self.user,
            title='Django Book',
            price=29.99
        )

    def test_index_view_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Book')

    def test_browse_view_loads(self):
        response = self.client.get(reverse('browse'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Book')

    def test_detail_view_loads(self):
        response = self.client.get(reverse('detail', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Book')

    def test_unauthenticated_user_redirected_from_new_item(self):
        """Unauthenticated user trying to create an item should be redirected to login page."""
        response = self.client.get(reverse('new_item'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_unauthenticated_user_redirected_from_inbox(self):
        """Unauthenticated user trying to access inbox should be redirected to login page."""
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
