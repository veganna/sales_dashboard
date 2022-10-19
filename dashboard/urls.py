from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardPage.as_view(), name='dashboard'),
    path('products/', ProductOverviewPage.as_view(), name='products'),
    path('products/product-simple/', EditProductSimple.as_view(), name='create-product-simple'),
    path('products/edit-product-variable', EditProductVariable.as_view(), name='edit-product-variable'),
    path('products/edit-product-digital', EditProductDigital.as_view(), name='edit-product-digital'),
    path('settings/', AdminSettings.as_view(), name='admin-settings'),
    path('login/', AdminLogin.as_view(), name='admin-login'),
    path('customers/', Customers.as_view(), name='customers'),
    path('customer-details/', CustomerDetail.as_view(), name='customer-details'),
    path('orders/', Orders.as_view(), name='orders'),
    path('order-details/', OrderDetail.as_view(), name='order-details'),
    path('subscriptions/', Subscriptions.as_view(), name='subscriptions'),
    path('subscription-details/', SubscriptionDetail.as_view(), name='subscription-details'),
    path('subscribers/', Subscribers.as_view(), name='subscribers'),
    path('subscriber-details/', SubscriberDetail.as_view(), name='subscriber-details'),

]