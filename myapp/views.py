from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import serializers, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    EmailSerializer,
    ProductSerializer,
    UserSerializer,
)
from myapp.tasks import schedule_email_task
from django.core.cache import cache


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_destroy(self, instance):
        if instance.subcategories.exists():
            raise serializers.ValidationError(
                "Cannot delete a category that has subcategories."
            )
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": "object deleted successfully",
            },
            status=status.HTTP_200_OK,
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)
        return Response(
            {
                "message": "object deleted successfully",
            },
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class EmailUser(viewsets.ModelViewSet):
    def create(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            schedule_email_task.delay(email)
            return Response(
                {"message": "You will receive an email shortly"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def send_mail(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            send_time = datetime.now() + timedelta(seconds=120)
            schedule_email_task.apply_async((email,), eta=send_time)
            return Response(
                {"message": "You will receive an email shortly"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(views.APIView):
    def get(self, request):
        products = cache.get("products")
        if not products:
            products = Product.objects.all()
            cache.set("products", products, timeout=60)
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
