from django.contrib.auth.models import User
from rest_framework import serializers

from myapp.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate(self, data):
        name = data.get("name")
        parent = data.get("parent", None)

        if Category.objects.filter(name=name, parent=parent).exists():
            raise serializers.ValidationError(
                "A category with this name and parent already exists."
            )

        return data

    def create(self, validated_data):
        name = validated_data.get("name")
        parent = validated_data.get("parent", None)

        category, created = Category.objects.get_or_create(
            name=name, parent=parent, defaults=validated_data
        )
        if not created:
            for attr, value in validated_data.items():
                setattr(category, attr, value)
            category.save()

        return category

    def update(self, instance, validated_data):
        name = validated_data.get("name", instance.name)
        parent = validated_data.get("parent", instance.parent)

        if (
            Category.objects.filter(name=name, parent=parent)
            .exclude(pk=instance.pk)
            .exists()
        ):
            raise serializers.ValidationError(
                "A category with this name and parent already exists."
            )

        # Update the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        name = data.get("name")
        price = data.get("price", None)

        if Product.objects.filter(name=name, price=price).exists():
            raise serializers.ValidationError(
                "A Product with this name and price already exists."
            )

        return data

    def create(self, validated_data):
        categories = validated_data.pop("categories")
        product = Product.objects.create(**validated_data)
        product.categories.set(categories)
        return product

    def update(self, instance, validated_data):
        categories = validated_data.pop("categories")
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        instance.categories.set(categories)
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_active"]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
