from django.urls import path

from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.Store, name="store"),
    path('cart/', views.Cart, name="cart"),
    path('checkout/', views.Checkout, name="checkout"),

    path('update_item/', views.UpdateItem, name="update_item"),
    path('process_order/', views.ProcessOrder, name="process_order"),

]
