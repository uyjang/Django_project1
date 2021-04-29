from django.urls import path  # 2
from . import views  # 1
urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
]
