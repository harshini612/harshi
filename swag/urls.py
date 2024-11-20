from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage view
    path('register/', views.register, name='register'),  # Registration view
    path('login/', views.login, name='login'),  # Login view
    path('api/swag/list',views.swag_list,name='swag_list'),
    path ('api/swag/details/<int:id>/', views.swag_details,name='swag_details'),
    path('womens/', views.womens_views, name='womens'),
    path('mens/', views.mens_view, name='mens'),
    path('kids/', views.kids_view, name='kids'),
    path('electronics/', views.electronics_view, name='electronics'),
    path('accessories/', views.accessories_view, name='accessories'),
    path('categories/',views.categories_view ,name='categories'),
    path('cart/', views.cart_view, name='cart'),
     path('sales/', views.sales_view, name='sales'),
    path('costumercare/',views.costumercare_view ,name='costumercare'),
    path('search/',views. search_view, name='search_view'),
    path('autocomplete/',views. autocomplete_view, name='autocomplete'),
    path('becomeseller/',views.becomeseller_view,name='becomeseller'),
    path('arrival/',views.arrival_view,name='arrival'),
     path('sales/',views.sales_view,name='sales'),
     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
     path('cart/', views.view_cart, name='view_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]






