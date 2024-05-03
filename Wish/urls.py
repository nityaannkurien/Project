from django.urls import path
from .views import scrape_flipkart
from .views import scrape_clothing
from .views import scrape_clothing1
from .views import scrape_flipkart1
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
    path('main1/', views.main1, name='main1'),
    path('main2/', views.main2, name='main2'),
    path('main3/', views.main3, name='main3'),
    path('main4/', views.main4, name='main4'),
    path('api/', views.api_view, name='api'),  
    path("start-wishing/", views.start_wishing, name="start_wishing"),
    path('scrape/', scrape_flipkart, name='scrape_flipkart'),
    path('scrape_clothing/', scrape_clothing, name='scrape_clothing'),
    path('scrape1/', scrape_flipkart1, name='scrape_flipkart1'),
    path('scrape_clothing1/', scrape_clothing1, name='scrape_clothing1'),
    path('scrape2/', views.scrape_flipkart2, name='scrape_flipkart2'),
    path('scrape_clothing2/', views.scrape_clothing2, name='scrape_clothing2'),
    path('scrape3/', views.scrape_flipkart3, name='scrape_flipkart3'),
    path('scrape_clothing3/', views.scrape_clothing3, name='scrape_clothing3'),
    path('scrape4/', views.scrape_flipkart4, name='scrape_flipkart4'),
    path('scrape_clothing4/', views.scrape_clothing4, name='scrape_clothing4'),
    path('delete/<uuid:wishlist_id>/', views.deleteList, name='delete_list'),
]