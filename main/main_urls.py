from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name="start"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('balance/', views.balance, name="balance"),
    path('/logout', views.logout_user, name="logout"),
]
