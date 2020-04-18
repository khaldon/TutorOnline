from django.urls import path
<<<<<<< HEAD
from .views import FormWizardView,edit_course,CartView,add_to_cart,remove_from_cart,CheckoutView,PaymentView,MyCourses,add_to_wishlist
=======
from .views import (FormWizardView,edit_course,CartView,
                    add_to_cart,remove_from_cart,CheckoutView,PaymentView
                    ,MyCourses,CoursesList, Wishlist)
>>>>>>> a94f7f4b649f0e32c49f2a07c1aae5de2ea508b7

app_name = 'courses'

urlpatterns = [
    path('add_course_to_wishlist/<slug>/',add_to_wishlist,name='add_to_wishlist'),
    path('create_course/',FormWizardView.as_view(),name='create_course'),
    path('my_courses/', MyCourses.as_view(), name='my_courses'),
    path('edit_course/<course>/',edit_course,name='edit_course'),
    path('wishlist/', Wishlist.as_view(), name='wishlist'),
    path('<username>/courses/',MyCourses.as_view(),name='my_courses'),
    path('cart/',CartView.as_view(),name='cart'),
    path('add_to_cart/<int:pk>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',remove_from_cart,name='remove_from_cart'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('payment/',PaymentView.as_view(),name='payment'),
    path('courses/',CoursesList.as_view(),name='courses')
]
