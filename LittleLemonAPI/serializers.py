from rest_framework import serializers
from . import models
from django.contrib.auth.models import User, Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = models.MenuItem
        fields = ['title','price','featured','category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

       
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['menuitem','quantity']
        read_only_fields = ['unit_price', 'price', 'user']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
    
     
