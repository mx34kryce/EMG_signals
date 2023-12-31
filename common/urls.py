from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.signup, name='signup'),
    path('to_mainpage/',views.to_mainpage,name='to_mainpage'),
    path('to_check/',views.to_check_manual,name='to_check'),
    path('check/',views.check,name='check'),
]
