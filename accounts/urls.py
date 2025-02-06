from django.urls import path
from . import views
from django.contrib.auth.views import  PasswordChangeView, PasswordChangeDoneView

app_name='accounts'
urlpatterns = [
            path('register/', views.UserRegisterView.as_view(), name='register'),
            path('login/', views.UserLoginView.as_view(), name='login'),
            path('logout/', views.UserLogoutView.as_view(), name='logout'),
            path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
            path('profile/update/<int:user_id>/', views.UpdateProfileView.as_view(), name='update'),
            path('profile/<int:user_id>/password-change/', PasswordChangeView.as_view(template_name='accounts/password/password_change.html'), name='password_change'),
            path('password-change-done/', PasswordChangeDoneView.as_view(template_name='accounts/password/password_change_done.html'),name='password_change_done'),
               ]
