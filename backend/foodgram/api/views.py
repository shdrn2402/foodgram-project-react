from api import filters, models, permissions, serializers
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.pagination import LimitPageNumberPagination


class TagViewSet(ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    pagination_class = None
    filterset_class = filters.IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsOwnerOrReadOnly]
    pagination_class = LimitPageNumberPagination
    filter_class = filters.AuthorTagFilter

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_name='favorite',
        url_path='favorite',
        permission_classes=[IsAuthenticated],
        serializer_class=serializers.FavoriteSerializers
    )
    def favorite(self, request, pk=id):
        if request.method == 'POST':
            user = request.user
            recipe = self.get_object()
            if models.Favorite.objects.filter(
                    user=user,
                    recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST)
            favorite = models.Favorite.objects.create(
                user=user,
                recipe=recipe)
            serializer = serializers.FavoriteSerializers(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(
                models.Favorite,
                user=request.user,
                recipe__id=pk
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_name='shopping_cart',
        url_path='shopping_cart',
        permission_classes=[IsAuthenticated],
        serializer_class=serializers.FavoriteSerializers
    )
    def shopping_cart(self, request, pk=id):
        if request.method == 'POST':
            user = request.user
            recipe = self.get_object()
            if models.Cart.objects.filter(
                    user=user,
                    recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже в корзине.'},
                    status=status.HTTP_400_BAD_REQUEST)
            favorite = models.Cart.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = serializers.FavoriteSerializers(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(
                models.Cart,
                user=request.user,
                recipe__id=pk
            )
            favorite.delete()
            return Response(
                f'Рецепт {favorite.recipe} удален из корзины {request.user}.',
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        url_name='download_shopping_cart',
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shoping_list = {}
        ingredients = models.RecipeIngredient.objects.filter(
            recipe__cart__user=request.user
        )
        for element in ingredients:
            shoping_list.setdefault(
                element.ingredient.name, {
                    'measurement_unit': element.ingredient.measurement_unit,
                    'amount': 0}
            )
            shoping_list[element.ingredient.name]['amount'] += element.amount

        to_buy = []
        for item in shoping_list:
            to_buy.append(
                f'{item} - {shoping_list[item]["amount"]}, '
                f'{shoping_list[item]["measurement_unit"]}' + '\n'
            )
        response = HttpResponse(to_buy, 'Content-Type: text/plain')
        response['Content-Disposition'] = (
            'attachment;' 'filename="to_buy.txt"'
        )
        return response
