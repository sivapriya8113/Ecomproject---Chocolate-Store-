from .models import Chocolates,Category
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ChocoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chocolates
        fields = '__all__'
        #fields = ('id','category', 'description', 'price','image_url','choco_available')




'''class AddtoSerializer(serializers.ModelSerializer):
    class Meta:
        model= CartItem'''