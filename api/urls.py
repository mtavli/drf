from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    CategoryListView,
    ProductListView,
    ProductDetailView,
    UserProductView,
    UserProductDetailView,
    ProductImageListView,
    ProductImageDetailView,
)


urlpatterns = [

    # USER

    path(
        "user/register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "user/login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "user/profile/",
        ProfileView.as_view(),
        name="profile"
    ),

    # CATEGORIES

    path(
        "categories/",
        CategoryListView.as_view(),
        name="categories"
    ),

    # PRODUCTS

    path(
        "products/",
        ProductListView.as_view(),
        name="products"
    ),

    path(
        "products/<int:product_id>/",
        ProductDetailView.as_view(),
        name="product-detail"
    ),

    # USER PRODUCTS

    path(
        "user/products/",
        UserProductView.as_view(),
        name="user-products"
    ),

    path(
        "user/products/<int:product_id>/",
        UserProductDetailView.as_view(),
        name="user-product-detail"
    ),

    # PRODUCT IMAGES

    path(
        "user/products/<int:product_id>/images/",
        ProductImageListView.as_view(),
        name="product-images"
    ),

    path(
        "user/products/<int:product_id>/images/<int:image_id>/",
        ProductImageDetailView.as_view(),
        name="product-image-detail"
    ),
]