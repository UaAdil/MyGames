from django.contrib import admin
from .models import Category, BoardGame

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'get_categories']
    list_filter = ['categories']
    search_fields = ('name',)

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])

    get_categories.short_description = 'Категории'
