from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.views import CategoriesViewSet, RecordsViewSet

# Crear el router para los ViewSets
router = DefaultRouter()
router.register(r"categories", CategoriesViewSet, basename="category")
router.register(r"records", RecordsViewSet, basename="record")

# URLs de la API
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
