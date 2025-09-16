from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CategoryView.as_view()),
    path('category/title/<str:title>/', views.CategoryDetailView.as_view()),
    path('menu-items/', views.MenuItemView.as_view()),
]