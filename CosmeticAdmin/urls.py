"CosmeticAdmin App Url"

from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('', views.Admin_dashboard, name='Admin_dashboard'),
    path('AddProduct/', views.AddProduct, name='AddProduct'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('register_subuser/', views.register_subuser, name='register_subuser'),    
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_edit/<int:id>/', views.admin_edit, name='admin_edit'),
    path('subadmin_login/', views.subadmin_login, name='subadmin_login'),
    path('subadmin_logout/', views.subadmin_logout, name='subadmin_logout'),
    path('Subadmin_dashboard/', views.Subadmin_dashboard, name='Subadmin_dashboard'),
    path('subadmin_edit/<int:id>/', views.subadmin_edit, name='subadmin_edit'),
    path('view_subuser/', views.view_subuser, name='view_subuser'),
    path('delete_subuser/<int:sid>/', views.delete_subuser, name='delete_subuser'),
    path('viewProducts/', views.viewProducts, name='viewProducts'),
    path('delete_product/<int:pid>/', views.delete_product, name='delete_product'),
    path('myorders/', views.myorders, name='myorders'),
    path('status/<int:id>/', views.status, name='status'),
    path('update_product/<int:pid>/', views.update_product, name='update_product'),
]

