from django.urls import path
from . import views
from .views import logout_view
from .views import favorites_view, toggle_favorite

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('ajax/search/', views.ajax_search, name='ajax_search'),
    path('contacts/', views.contacts, name='contacts'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    path('checkout/', views.checkout_view, name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),


    path('favorites/', favorites_view, name='favorites'),
    path('favorites/toggle/<int:pk>/', toggle_favorite, name='toggle_favorite'),

    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),

]
