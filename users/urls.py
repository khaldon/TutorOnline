from django.urls import path,include,reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import SignUpView,StudentSignUpView,TeacherSignUpView,profile,delete_user
from .forms import CustomAuthForm

app_name = 'users'

urlpatterns = [
    path('accounts/signup/',SignUpView.as_view(),name='signup'),
    path('accounts/signup/student/',StudentSignUpView.as_view(),name='student_signup'),
    path('accounts/signup/teacher/',TeacherSignUpView.as_view(),name='teacher_signup'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthForm),name='login',),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('password-change/',login_required(auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('users:password_change_done'))),name='password_change'),
    path('password-change/done/',login_required(auth_views.PasswordChangeDoneView.as_view()),name='password_change_done'),
    path('password-reset/',auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url = reverse_lazy('users:password_reset_complete')),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('profile/', profile, name='profile'),
    path('delete/<username>/',delete_user,name='delete_user'),
]
