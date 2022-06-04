from api import views
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('ingredients', views.IngredientViewSet)
router.register('tags', views.TagViewSet)
router.register('recipes', views.RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]
