from rest_framework import serializers
from .models import Post, Comment


class PostModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['post', 'text', 'parent', 'is_child']

