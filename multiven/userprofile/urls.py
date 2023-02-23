from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # django  in built login---------------------------------------
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    # django  in built logout---------------------------------------
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('clear/', views.clear, name='clear'),
    path('my_store/', views.my_store, name='my_store'),
    path('my_store/order_detail/<int:pk>/', views.my_store_order_detail, name='my_store_order_detail'),
    path('my_store/add_product/', views.add_product, name='add_product'),
    path('my_store/edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my_store/delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]