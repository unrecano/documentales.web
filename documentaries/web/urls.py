"""
Urls for Documentary project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('documentaries/<slug:slug>/', views.DocumentaryDetailView.as_view(),
        name="detail"),
    path('about/', views.AboutView.as_view(), name="about"),
    path('urls/<uuid:id>/', views.ToSiteRedirectView.as_view(),
        name="redirect"),
    path('report/', views.ReportDocumentaryView.as_view(), name="report"),
    path('', views.SearchDocumentaryView.as_view(), name="search")
]
