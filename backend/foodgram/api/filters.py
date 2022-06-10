import django_filters
from api import models
from django_filters.rest_framework import CharFilter, FilterSet


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='istartswith')

    class Meta:
        model = models.Ingredient
        fields = ['name', 'measurement_unit']


class AuthorTagFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    is_favorited = CharFilter(method='filter_is_favorited')
    is_in_shopping_cart = CharFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = models.Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_tags(self, queryset, slug, tags):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(tags__slug__in=tags).distinct()

    def _is_favorited_is_in_shopping_cart(self, queryset, key):
        filter_dict = {'favorites': 'is_favorited',
                       'cart': 'is_in_shopping_cart'
                       }
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        value = self.request.query_params.get(filter_dict[key], )
        if value:
            return queryset.filter(
                **{f'{key}__user': self.request.user}
            ).distinct()
        return queryset

    def filter_is_favorited(self, queryset, is_favorited, slug):
        return self._is_favorited_is_in_shopping_cart(queryset, 'favorites')

    def filter_is_in_shopping_cart(self, queryset, is_in_shopping_cart, slug):
        return self._is_favorited_is_in_shopping_cart(queryset, 'cart')
