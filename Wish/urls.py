from django.urls import path
from .views import scrape_flipkart

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.loginUser, name='login'),
    path('signup/',views.signup, name='signup'),
    path('create/', views.create, name='create'),
    path('logout/', views.logoutUser, name='logout'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('wishing/', views.create_wishlist, name='create_wishlist'),
    path('', views.index, name='index'),
    path('main/', views.main, name='main'),
    path('api/', views.api_view, name='api'),  
    path("start-wishing/", views.start_wishing, name="start_wishing"),
    path('scrape/', scrape_flipkart, name='scrape_flipkart'),
   
]