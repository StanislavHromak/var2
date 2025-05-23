from django.shortcuts import render
from .models import Recipe, Category
from django.db.models import Count

def main(request):
    """
    Виводить останні 5 сторінок на головну сторінку
    """
    recipes = Recipe.objects.order_by('-created_at')[:5]
    return render(request, 'main.html', {'recipes': recipes})

def category_list(request):
    """
    Виводить всі категорії з кількістю рецептів для кожного
    """
    categories = Category.objects.annotate(recipe_count=Count('categories'))
    return render(request, 'category_list.html', {'categories': categories})
