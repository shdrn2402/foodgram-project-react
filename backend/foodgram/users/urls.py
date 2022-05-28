from django.urls import include, path, re_path
from djoser import views as djoser_views
from rest_framework import routers
from users import views as users_views

app_name = 'users'

router = routers.DefaultRouter()
router.register('users', users_views.CustomUserViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/',
         users_views.CustomTokenCreateView.as_view(), name='login'),
    path('auth/token/logout/',
         djoser_views.TokenDestroyView.as_view(), name='logout'),
]
