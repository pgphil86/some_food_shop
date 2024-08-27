from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from products.views import (CategoryListView,
                            CartView,
                            ProductListView,
                            SubcategoryListView
                            )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoryListView.as_view(),
         name='category-list'),
    path('subcategories/', SubcategoryListView.as_view(),
         name='subcategory-list'),
    path('products/', ProductListView.as_view(),
         name='product-list'),
    path('cart/', CartView.as_view(),
         name='cart'),
    path('cart/clear/', CartView.as_view(),
         name='cart-clear'),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
