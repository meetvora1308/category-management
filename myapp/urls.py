from django.urls import include, path
from rest_framework.routers import DefaultRouter

from myapp import views

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"product", views.ProductViewSet)
router.register(r"emaiuser", views.EmailUser, basename="emailuser")
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
    path("products_cache/", views.ProductListView.as_view(), name="product-list"),
    path("", include(router.urls)),
]
