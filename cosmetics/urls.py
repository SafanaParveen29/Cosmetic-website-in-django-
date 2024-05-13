"""App Url"""

from django.urls import path
from . import views

urlpatterns = [
    path('header/', views.header, name='header'),
    path('footer/', views.footer, name='footer'),
    path('', views.body, name='body'),
    path('product/', views.product, name='product'),
    path('viewProduct/<int:id>/', views.viewProduct, name='viewProduct'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),    
    path('user_logout/', views.user_logout, name='user_logout'),
    path('edit_users/<int:id>/', views.edit_users, name='edit_users'),
    path('wishlist/', views.wishlist, name='wishlist'),    
    path('cart/', views.cart, name='cart'),
    path('addcart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('removecart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),    
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'), 
    path('category/<str:category>/',views.products_by_category,name='products_by_category'),
]
