from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    path('logout/', LogoutView.as_view(), name='logout'),
]
