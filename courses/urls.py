from django.urls import path
from .views import (FormWizardView,edit_course,CartView,
                    add_to_cart,remove_from_cart,CheckoutView,PaymentView,
                    MyCourses,CoursesList, WishListView, CourseView, add_to_wishlist,
                    add_section_to_course,add_video_to_section,course_search,course_filter)

app_name = 'courses'

urlpatterns = [
    path('add_course_to_wishlist/<slug>/',add_to_wishlist,name='add_to_wishlist'),
    path('create_course/',FormWizardView.as_view(),name='create_course'),
    path('search/',course_search, name='course_search'),
    path('my_courses/', MyCourses.as_view(), name='my_courses'),
    path('edit_course/<course>/',edit_course,name='edit_course'),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('<username>/courses/',MyCourses.as_view(),name='my_courses'),
    path('cart/',CartView.as_view(),name='cart'),
    path('add_to_cart/<int:pk>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',remove_from_cart,name='remove_from_cart'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('payment/',PaymentView.as_view(),name='payment'),
    path('courses/',CoursesList.as_view(),name='courses'),
    path('course/<slug>/', CourseView, name='course_detail'),
    path('section/add/',add_section_to_course,name='add_section_to_course'),
    path('video/add/',add_video_to_section,name='add_video_to_section'),
    path('filter/', course_filter, name='course_filter')
]
