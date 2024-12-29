from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(), name='register'),
    path('',views.UserLoginView.as_view(), name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('profile/',views.profile, name='profile'),
    path('profile/change_password/',views.pass_change, name='change_password'),
    path('profile/pass_change_without_old/',views.pass_change_without_old, name='pass_change_without_old'),
]
