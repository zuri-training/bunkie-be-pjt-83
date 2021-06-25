from rest_framework import serializers
from .models import Room,User,Comment
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



########################### comment section ##########################################
class RoomSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='landlord.first_name')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_type', 'description', 'university', 'owner', 'comments']

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'posts', 'comments']

class CommentSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.email')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'name', 'post']
