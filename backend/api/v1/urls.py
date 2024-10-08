from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)
from rest_framework.routers import DefaultRouter

from .views.slot_view import SlotViewSet
from .views.user_view import UserRegistrationViewSet
from .views.user_view import UserViewSet

v1_router = DefaultRouter()
v1_router.register('slots', SlotViewSet, basename='slots')
v1_router.register('users', UserViewSet, basename='users')
v1_router.register(r'register', UserRegistrationViewSet, basename='user-register')

urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include('djoser.urls.jwt')),
]

urlpatterns += [
    path(
        'schema/',
        SpectacularAPIView.as_view(api_version='api/v1'),
        name='schema'
    ),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]
