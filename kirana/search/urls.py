from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchDocumentaryView.as_view(), name="search")
]