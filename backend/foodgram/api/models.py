from django.core import validators
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=250, unique=True, verbose_name='Название ярлыка'
    )
    color = models.CharField(
        max_length=50, unique=True, verbose_name='Цвет ярлыка'
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name='Идентификатор ярлыка'
    )

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'Tags managment'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'Ingredients managment'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Ярлыки',
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение рецепта'
    )
    text = models.TextField(
        verbose_name='Рецепт'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                1, message='Бытрее минуты? Серьезно?'),
        ],
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'recipe'
        verbose_name_plural = 'Recipes managment'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Название ингредиента'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                1, message='Каша из ничего?'
            )
        ],
        verbose_name='Количество ингредиента',
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'Ingredients managment'

    def __str__(self):
        return f'Ингредиент: {self.ingredient.name},рецепт: {self.recipe.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'favorite recipes',
        verbose_name_plural = 'Favorite recipes managment'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite recipe'
            )
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'cart'
        verbose_name_plural = 'Cart managment'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique cart')
        ]
