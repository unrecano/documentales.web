from django.urls import path
from . import views

urlpatterns = [
    path('documentaries/<slug:slug>/', views.detail, name="detail"),
    path('about', views.AboutView.as_view(), name="about"),
    path('urls/<uuid:id>/', views.RedirectSiteView.as_view(), name="redirect"),
    path('point', views.point, name="point")
]