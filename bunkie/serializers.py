from rest_framework import serializers
from .models import Room
import django_filters


########## Search filter Serializer ##############
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = ['state', 'university', 'type_of_apartment','price']
