from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe, Category
from django.utils import timezone
from datetime import timedelta


class RecipeViewsTestCase(TestCase):
    def setUp(self):
        """
        Set up test data: create categories and recipes.
        """
        self.client = Client()
        self.category1 = Category.objects.create(name="Desserts")
        self.category2 = Category.objects.create(name="Main Dishes")

        # Create 6 recipes with explicit created_at times
        base_time = timezone.now()
        for i in range(6):
            Recipe.objects.create(
                title=f"Recipe {i + 1}",
                description=f"Description for recipe {i + 1}",
                instructions="Mix and cook.",
                ingredients="Flour, sugar, eggs",
                category=self.category1 if i % 2 == 0 else self.category2,
                created_at=base_time - timedelta(seconds=i)  # Використовуємо секунди для чіткого порядку
            )

    def test_main_view(self):
        """
        Test the main view: should display the 5 latest recipes.
        """
        response = self.client.get(reverse('recipe:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertEqual(len(response.context['recipes']), 5)
        recipes = response.context['recipes']
        self.assertEqual(recipes[0].title, "Recipe 1")  # Найновіший
        self.assertEqual(recipes[4].title, "Recipe 5")  # П’ятий за новизною
        self.assertContains(response, "Recipe 1")
        self.assertContains(response, "Description for recipe 1")

    def test_main_view_no_recipes(self):
        """
        Test the main view when no recipes exist.
        """
        Recipe.objects.all().delete()
        response = self.client.get(reverse('recipe:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertEqual(len(response.context['recipes']), 0)
        self.assertContains(response, "No recipes found.")

    def test_category_list_view(self):
        """
        Test the category list view: should display all categories with recipe counts.
        """
        response = self.client.get(reverse('recipe:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')
        categories = response.context['categories']
        self.assertEqual(len(categories), 2)
        for category in categories:
            if category.name == "Desserts":
                self.assertEqual(category.recipe_count, 3)
            elif category.name == "Main Dishes":
                self.assertEqual(category.recipe_count, 3)
        self.assertContains(response, "Desserts (3 recipes)")
        self.assertContains(response, "Main Dishes (3 recipes)")

    def test_category_list_view_no_categories(self):
        """
        Test the category list view when no categories exist.
        """
        Category.objects.all().delete()
        response = self.client.get(reverse('recipe:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')
        self.assertEqual(len(response.context['categories']), 0)
        self.assertContains(response, "No categories found.")
