from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductImageSerializer
)

from .models import Category, Product, ProductImage

from .filters import ProductFilter


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "User created successfully.",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:

            return Response(
                {
                    "detail": "Username and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response(
                {
                    "detail": "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )


# CATEGORY

class CategoryListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(
            serializer.data
        )


# PRODUCTS

class ProductListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        products = Product.objects.filter(
            is_active=True
        ).order_by("-created_at")

        product_filter = ProductFilter( # filter the products based on query parameters
            request.GET,
            queryset=products
        )

        products = product_filter.qs


         # order the products based on the ordering query parameter
         
        ordering = request.GET.get("ordering")

        allowed_ordering = [
            "price",
            "-price",
            "created_at",
            "-created_at",
            "title",
            "-title"
        ]

        if ordering in allowed_ordering:

            products = products.order_by(
                ordering
            )
            
            
        # paginate the products using PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 5

        page = paginator.paginate_queryset(
            products,
            request
        )

        serializer = ProductSerializer(
            # products,
            page, # artık page değişkenini kullanıyoruz
            many=True
        )

 # Pagination için return Response(serializer.data) yerine aşağıdaki kodu kullanın
        # return Response(
        #     serializer.data
        # )
        
        return paginator.get_paginated_response(
            serializer.data
        )


class ProductDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, product_id):

        try:

            product = Product.objects.get(
                id=product_id,
                is_active=True
            )

        except Product.DoesNotExist:

            return Response(
                {
                    "detail": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product
        )

        return Response(
            serializer.data
        )


# USER PRODUCTS

class UserProductView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        products = Product.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            product = serializer.save(
                user=request.user
            )

            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProductDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_product(self, product_id, user):

        try:

            return Product.objects.get(
                id=product_id,
                user=user
            )

        except Product.DoesNotExist:

            return None

    def put(self, request, product_id):

        product = self.get_product(
            product_id,
            request.user
        )

        if product is None:

            return Response(
                {
                    "detail": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, product_id):

        product = self.get_product(
            product_id,
            request.user
        )

        if product is None:

            return Response(
                {
                    "detail": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# PRODUCT IMAGES

class ProductImageListView(APIView):

    permission_classes = [IsAuthenticated]

    def get_product(self, product_id, user):

        try:

            return Product.objects.get(
                id=product_id,
                user=user
            )

        except Product.DoesNotExist:

            return None

    def get(self, request, product_id):

        product = self.get_product(
            product_id,
            request.user
        )

        if product is None:

            return Response(
                {
                    "detail": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        images = ProductImage.objects.filter(
            product=product
        ).order_by(
            "-is_main",
            "created_at"
        )

        serializer = ProductImageSerializer(
            images,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request, product_id):

        product = self.get_product(
            product_id,
            request.user
        )

        if product is None:

            return Response(
                {
                    "detail": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductImageSerializer(
            data=request.data,
            context={
                "product": product
            }
        )

        if serializer.is_valid():

            image = serializer.save()

            return Response(
                ProductImageSerializer(
                    image
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


        try:

            return Product.objects.get(
                id=product_id,
                user=user
            )

        except Product.DoesNotExist:

            return None


class ProductImageDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_image(self, product_id, image_id, user):

        try:

            return ProductImage.objects.get(
                id=image_id,
                product__id=product_id,
                product__user=user
            )

        except ProductImage.DoesNotExist:

            return None

    def patch(self, request, product_id, image_id):

        image = self.get_image(
            product_id,
            image_id,
            request.user
        )

        if image is None:

            return Response(
                {
                    "detail": "Image not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductImageSerializer(
            image,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            image = serializer.save()

            return Response(
                ProductImageSerializer(image).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, product_id, image_id):

        image = self.get_image(
            product_id,
            image_id,
            request.user
        )

        if image is None:

            return Response(
                {
                    "detail": "Image not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        image.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )