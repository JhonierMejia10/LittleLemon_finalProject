from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CategoryView.as_view()),
    path('category/title/<str:title>/', views.CategoryDetailView.as_view()),
    path('menu-items/', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view()),
    path('menu-items/items/<int:pk>/', views.MenuItemForAll.as_view()),
    path('groups/gestor/users/', views.ManagerUsersView.as_view()),
    path('groups/gestor/users/<int:pk>/', views.DeleteUserFromManager.as_view()),
    path('groups/delivery-crew/users/', views.DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>/', views.DeliveryCrewDestroyView.as_view()),
    path('cart/menu-items', views.CartMenuItemsView.as_view(), name='Menu-items-car'),
    path('orders/', views.OrderView.as_view(), name='Orders'),
    path('orders/<int:pk>/', views.OrderViewDetail.as_view(), name='Order detail')
]