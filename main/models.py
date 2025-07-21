from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BoardGame(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название игры")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="В наличии")
    categories = models.ManyToManyField(Category, related_name='games', verbose_name="Категории")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    players = models.CharField(max_length=20, blank=True, verbose_name="Количество игроков")
    duration = models.CharField(max_length=50, blank=True, verbose_name="Время игры")
    age = models.CharField(max_length=20, blank=True, verbose_name="Возраст")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    is_best = models.BooleanField(default=False, verbose_name="Хит")
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="Скидка (%)")

    def __str__(self):
        return self.name
