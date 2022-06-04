from djoser import serializers as djoser_serializers
from djoser import utils, views
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users import models, pagination, serializers


class CustomTokenCreateView(views.TokenCreateView):

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = djoser_serializers.TokenSerializer
        return Response(
            data=token_serializer_class(
                token).data, status=status.HTTP_201_CREATED
        )


class CustomUserViewset(views.UserViewSet):
    pagination_class = pagination.LimitPageNumberPagination

    @action(
        detail=False,
        methods=['GET'],
        url_name="subscriptions",
        url_path="subscriptions",
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = models.Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = serializers.FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_name="subscribe",
        url_path="subscribe",
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            user = request.user
            author = get_object_or_404(models.User, id=id)
            if user == author:
                return Response(
                    {'errors': 'Кроме себя любимого есть и другие авторы.'},
                    status=status.HTTP_400_BAD_REQUEST)
            if models.Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST)
            follow = models.Follow.objects.create(user=user, author=author)
            serializer = serializers.FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            author = get_object_or_404(models.User, id=id)
            if user == author:
                return Response({
                    'errors': 'Нельзя отписаться от самого себя.'
                })
            follow = models.Follow.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.data, {
                'errors': 'Вы не подписаны на этого автора.'
            })
        return Response(status=status.HTTP_204_NO_CONTENT)
