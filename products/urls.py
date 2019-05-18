from django.urls import path

from .views import (
    ProductListView,
    ProductDetailSlugView,
    ProductFeaturedListView,
    ProductFeaturedDetailView)

app_name = 'products'

urlpatterns = [
    path(r'products/', ProductListView.as_view(), name='products'),
    path(r'products/<slug>/', ProductDetailSlugView.as_view(), name='detail'),
    path(r'featured/', ProductFeaturedListView.as_view()),
    path(r'featured/<pk>/', ProductFeaturedDetailView.as_view())
]