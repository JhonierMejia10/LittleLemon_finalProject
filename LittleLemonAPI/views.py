from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers
from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework import status



# Endpoints para Menuitems

class MenuItemView(generics.ListAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer

    def get_queryset(self):
            category_id = self.request.query_params.get('category')
            if category_id:
                return models.MenuItem.objects.filter(category_id=category_id)
            return models.MenuItem.objects.all()


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


