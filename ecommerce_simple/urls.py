from django.urls import path
from . import views
app_name = 'Ecommerce'

urlpatterns = [
    path('products/get-products/', views.GetAllProductsView.as_view(), name='get-all-products'),
    path('products/get-products/<int:id>/', views.GetProductView.as_view(), name='get-product-by-id'),
    path('products/filter-products/', views.FilterProductsView.as_view(), name='filter-products'),
    path('products/utils/get-categories/', views.GetAllCategoriesView.as_view(), name='get-all-categories'),
    path('cart/get-cart/', views.GetCart.as_view(), name='get-cart'),
    path('cart/add-to-cart/', views.AddToCart.as_view(), name='add-to-cart'),
    path('cart/remove-from-cart/', views.RemoveFromCart.as_view(), name='remove-from-cart'),
    path('cart/empty-cart/', views.DeleteCart.as_view(), name='empty-cart'),
    path('order/create-order/', views.CreateOrder.as_view(), name='create-order'),
    path('order/get-orders/', views.GetOrder.as_view(), name='get-orders'),
    path('order/get-order/<int:order_id>/', views.GetOrderById.as_view(), name='get-order'),
    path('order/delete-order/<int:order_id>/', views.DeleteOrder.as_view(), name='delete-order'),
    
]