from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Band(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=150)
    band_id = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='albums')

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=250)
    duration = models.IntegerField()
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')

    def __str__(self) -> str:
        return self.name

class AlbumReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField('content')
    score = models.IntegerField('score')

    def __str__(self) -> str:
        return f'{self.album_id.name} Review'

class AlbumReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_review_id = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('content')

class AlbumReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_review_id = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name='likes')