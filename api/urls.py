from django.urls import path

from .views import (
    CartItemCreateView,
    CartItemDetailView,
    CartView,
    FavoriteListView,
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
        "favorites/",
        FavoriteListView.as_view(),
        name="favorites"
    ),
    path(
        "favorites/<int:product_id>/",
        FavoriteListView.as_view(),
        name="favorite-detail"
    ),
    path(
        "cart/",
        CartView.as_view(),
        name="cart"
    ),
    path(
     "cart/items/<int:item_id>/",
      CartItemDetailView.as_view(),
    name="cart-item-detail"
    ),
    path(
        "cart/items/",
        CartItemCreateView.as_view(),
        name="cart-item-create"
    )
]