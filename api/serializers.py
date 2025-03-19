from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username',read_only = True)
    class Meta:
        model = Post
        fields = ('id','title','author_name')

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"