from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers
from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework import status
from . import permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.utils import timezone


# Endpoints para Menuitems

class MenuItemView(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsGestor]

    def get_queryset(self):
            category_id = self.request.query_params.get('category')
            if category_id:
                return models.MenuItem.objects.filter(category_id=category_id)
            return models.MenuItem.objects.all()

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
     queryset = models.MenuItem.objects.all()
     serializer_class = serializers.MenuItemSerializer
     permission_classes = [permissions.IsGestor, IsAuthenticated]

class MenuItemForAll(generics.RetrieveAPIView):
     queryset = models.MenuItem.objects.all()
     serializer_class = serializers.MenuItemSerializer
     


# Endpoints para categorías 
class CategoryView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'title'

    def get(self, request, *args, **kwargs):
        title = kwargs.get('title')
        try: 
            category = self.get_object()
            serializer = self.get_serializer(category)
            return Response(serializer.data)
        except:
            return Response({'error': f'La categoría con el título "{title}" no existe.'}, status=status.HTTP_404_NOT_FOUND)


# Endpoints para grupo gestor

class ManagerUsersView(APIView):
     permission_classes = [permissions.IsGestor, IsAuthenticated]

     def get(self, request):
          users = User.objects.filter(groups__name='Gestor')
          serializer = serializers.UserSerializer(users, many=True)
          return Response(serializer.data) 
     
     def post(self, request):
          serializer = serializers.UserSerializer(data=request.data)
          if serializer.is_valid():
               user = serializer.save()
               gestor_group = Group.objects.get(name='Gestor')
               user.groups.add(gestor_group)
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
     #def delete(self, request, user_id):
     #     try: 
     #          user = User.objects.get(id=user_id)
     #          user.delete()
     #          return Response(status=status.HTTP_200_OK)
     #     except User.DoesNotExist:
     #          return Response(status=status.HTTP_404_BAD_REQUEST)


# Se utilizó esta clase siguiendo las instrucciones del proyecto 
class DeleteUserFromManager(generics.DestroyAPIView):
     queryset = User.objects.all()
     permission_classes = [permissions.IsGestor, IsAuthenticated]


# Endpoints para grupo Equipo de entrega

class DeliveryCrewView(generics.ListCreateAPIView):
     queryset = User.objects.filter(groups__name='Equipo de entrega')
     serializer_class = serializers.UserSerializer
     permission_classes = [permissions.IsGestor]


class DeliveryCrewDestroyView(generics.DestroyAPIView):
     queryset = User.objects.filter(groups__name='Equipo de entrega')
     permission_classes = [permissions.IsGestor,IsAuthenticated]


class CartMenuItemsView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return models.Cart.objects.filter(user=self.request.user)     
    
    def perform_create(self, serializer):
        menuitem = serializer.validated_data['menuitem']
        quantity = serializer.validated_data['quantity']
        
        serializer.save(
            user=self.request.user,
            unit_price=menuitem.price,
            price=menuitem.price * quantity
        )

    def delete(self, request, *args, **kwargs):
        models.Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class OrderView(generics.ListCreateAPIView):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Gestor').exists():
            return models.Order.objects.all()
        
        elif user.groups.filter(name='Equipo de entrega').exists():
            return models.Order.objects.filter(delivery_crew=user)
            
        else:
            return models.Order.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = models.Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"detail": "El carrito está vacío."}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.menuitem.price for item in cart_items) 
        order_data = {
            'user': user.id,
            'total': total,
            'date': timezone.now().date(),  
            'items': [item.menuitem.id for item in cart_items] 
        }
        # Serializar y guardar la nueva orden
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        cart_items.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class OrderViewDetail(generics.RetrieveUpdateDestroyAPIView):
     queryset = models.Order
     serializer_class = serializers.OrderSerializer