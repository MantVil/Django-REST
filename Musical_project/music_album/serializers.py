from rest_framework import serializers
from .models import Band, Album, Song, AlbumReview, AlbumReviewComment, AlbumReviewLike

class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ['id', 'name']

class AlbumSerializer(serializers.ModelSerializer):
    band = serializers.CharField(read_only=False, source='band_id.name')

    class Meta:
        model = Album
        fields = ['id', 'band_id', 'band', 'name']

class SongSerializer(serializers.ModelSerializer):
    album_name = serializers.CharField(read_only=False, source='album_id.name')
    band_name = serializers.CharField(
        read_only=False, source='album_id.band_id.name'
    )

    class Meta:
        model = Song
        fields = ['name', 'duration', 'album_id', 'album_name', 'band_name']

class AlbumReviewCommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    album_review_id = serializers.ReadOnlyField(source='album_review_id.id')

    class Meta:
        model = AlbumReviewComment
        fields = ['id', 'user_id', 'username', 'album_review_id', 'content']

class AlbumReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True, source='user_id.username')
    album_name = serializers.CharField(read_only=True, source='album_id.name')
    band_name = serializers.CharField(read_only=True, source='album_id.band_id.name')
    user_id = serializers.CharField(read_only=True, source='user_id.id')
    comments = AlbumReviewCommentSerializer(read_only=True, many=True)
    comment_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    
    class Meta:
        model = AlbumReview
        fields = ['id', 'user_id', 'user_name', 'album_id',
                  'album_name', 'band_name', 'content', 'score', 'comments', 'comment_count', 'likes']

    def get_comment_count(self, obj):
        return AlbumReviewComment.objects.filter(album_review_id=obj).count()

    def get_likes(self, obj):
        return AlbumReviewLike.objects.filter(album_review_id=obj).count()

class AlbumReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumReviewLike
        fields = ['id']
