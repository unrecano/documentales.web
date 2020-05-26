from django.urls import path
from . import views

urlpatterns = [
    path('documentaries/<slug:slug>/', views.detail, name="detail"),
    path('about', views.about, name="about")
]