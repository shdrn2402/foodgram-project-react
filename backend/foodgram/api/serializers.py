from api import models
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users import models as users_models
from users import serializers as users_serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = '__all__'


class RecipeIngredientSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = models.RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = users_serializers.CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializers(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time'
        )
        model = models.Recipe

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return models.Recipe.objects.filter(favorites__user=user,
                                            id=obj.id
                                            ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return models.Recipe.objects.filter(cart__user=user,
                                            id=obj.id
                                            ).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = self.initial_data.get('ingredients')
        tags_data = self.initial_data.get('tags')
        recipe = models.Recipe.objects.create(author=request.user,
                                              **validated_data
                                              )
        recipe.tags.set(tags_data)

        for ingredient in ingredients:
            amount = ingredient.get('amount')
            ingredient_instance = get_object_or_404(models.Ingredient,
                                                    pk=ingredient.get('id')
                                                    )
            models.RecipeIngredient.objects.bulk_create([
                models.RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient_instance,
                    amount=amount
                )
            ])

        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients = self.initial_data.get('ingredients')
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        models.RecipeIngredient.objects.filter(recipe=instance).all().delete()
        for ingredient in ingredients:
            models.RecipeIngredient.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

        instance.save()
        return instance


class FavoriteSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = Base64ImageField(source='recipe.image')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = models.Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = models.Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = users_models.Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return users_models.Follow.objects.filter(user=obj.user,
                                                  author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = models.Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return models.Recipe.objects.filter(author=obj.author).count()
