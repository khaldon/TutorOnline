from django.urls import path
from .views import create_course,edit_course,CartView,add_to_cart,remove_from_cart,CheckoutView,PaymentView

app_name = 'courses'

urlpatterns = [
    path('create_course/',create_course,name='create_course'),    
    path('edit_course/<course>/',edit_course,name='edit_course'),
    path('cart/',CartView.as_view(),name='cart'),
    path('add_to_cart/<int:pk>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',remove_from_cart,name='remove_from_cart'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('payment/',PaymentView.as_view(),name='payment'),
]
