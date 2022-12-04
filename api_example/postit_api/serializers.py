from rest_framework import serializers
from . import models

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = models.Comment
        fields = ('id', 'post', 'body', 'user', 'user_id', 'created_at')

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    # comments = serializers.StringRelatedField(many=True) 
    comments = CommentSerializer(many=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self,obj):
        return models.Comment.objects.filter(post=obj).count()

    class Meta:
        model = models.Post
        fields = ('id', 'title', 'body', 'user', 'user_id', 'created_at', 'comments', 
                'comments_count')

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        fields = ['id']