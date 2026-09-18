from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product , ProductImage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user
    
# PRODUCT

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "created_at"
        ]


# IMAGE

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = [
            "id",
            "image",
            "is_main",
            "created_at"
        ]

        read_only_fields = [
            "id",
            "created_at"
        ]

    def create(self, validated_data):

        product = self.context["product"]

        if validated_data.get("is_main", False):

            ProductImage.objects.filter(
                product=product
            ).update(
                is_main=False
            )

        return ProductImage.objects.create(
            product=product,
            **validated_data
        )

    def update(self, instance, validated_data):

        if validated_data.get("is_main", False):

            ProductImage.objects.filter(
                product=instance.product
            ).exclude(
                id=instance.id
            ).update(
                is_main=False
            )

        return super().update(
            instance,
            validated_data
        )


class ProductSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source="user.username")
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "user",
            "category",
            "title",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
            "is_active",
            "images" # EKLENDİ
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "images" # EKLENDİ
        ]