from django.core import validators
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name='Name'
    )
    color = models.CharField(
        max_length=50, unique=True, verbose_name='Color'
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'Tags managment'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Name'
    )
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Measurement unit'
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'Ingredients managment'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Author',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Recipe name'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Resipe image'
    )
    text = models.TextField(
        verbose_name='Recipe description'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                1, message='Бытрее минуты? Серьезно?'),
        ],
        verbose_name='Cooking time'
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
        related_name="+",
        verbose_name='Ingredient name'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name='Recipe'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                1, message='Каша из ничего?'
            )
        ],
        verbose_name='Amount',
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'Ingredients managment'

    def __str__(self):
        return self.ingredient.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Recipe'
    )

    class Meta:
        verbose_name = 'favorite recipe',
        verbose_name_plural = 'Favorite recipes managment'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite recipe for user'
            )
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Recipe',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'cart'
        verbose_name_plural = 'Cart managment'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique cart user')
        ]
