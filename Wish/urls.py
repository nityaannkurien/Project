from django.urls import path
from .views import scrape_amazon
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
    path('main/<str:wishlist_name>/', views.main, name='main'),
    path("start-wishing/", views.start_wishing, name="start_wishing"),
    path('scrapeflipkart/<str:wishlist>/', scrape_flipkart, name='scrapeflipkart'),
    path('scrapeamazon/<str:wishlist>/', scrape_amazon, name='scrapeamazon'),
    path('delete/<uuid:wishlist_id>/', views.deleteList, name='delete_list'),
    path('addtocart/<str:wishlist>/<str:product>/<str:price>/<path:image>/', views.addtocart, name='addtocart'),
    path('status_update/<str:wishlist_name>/<str:product_name>/<str:status>/', views.status_update, name='status_update'),
    path('delete_item/<str:wishlist_name>/<str:product_name>/', views.delete_item, name='delete_item'),
    path('sort_low_to_high/<str:wishlist>/', views.sort_low_to_high, name='sort_low_to_high'),
    path('sort_high_to_low/<str:wishlist>/', views.sort_high_to_low, name='sort_high_to_low'),
]
