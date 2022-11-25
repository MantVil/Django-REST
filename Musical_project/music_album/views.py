from django.shortcuts import render

from django.shortcuts import render
from django.views import generic
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Band, Album, Song, AlbumReview, AlbumReviewComment, AlbumReviewLike
from .serializers import AlbumReviewCommentSerializer, AlbumReviewLikeSerializer, BandSerializer, AlbumSerializer, SongSerializer, AlbumReviewSerializer

class BandList(generics.ListCreateAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer

class BandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Trinti gali tik administratorius!')

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError('Taisyti gali tik administratorius!')


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class AlbumReviewList(generics.ListCreateAPIView):
    queryset = AlbumReview.objects.all()
    serializer_class = AlbumReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class AlbumReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlbumReview.objects.all()
    serializer_class = AlbumReviewSerializer

    def delete(self, request, *args, **kwargs):
        review = AlbumReview.objects.filter(pk=kwargs['pk'], user_id=self.request.user)
        if review.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("Action forbidden! You're trying to delete someone else's review!")


    def put(self, request, *args, **kwargs):
        review = AlbumReview.objects.filter(pk=kwargs['pk'], user_id=self.request.user)
        if review.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError("Action forbidden! You're trying to edit someone else's review!")


class AlbumReviewCommentList(generics.ListCreateAPIView):
    queryset = AlbumReviewComment.objects.all()
    serializer_class = AlbumReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = AlbumReview.objects.get(pk=self.kwargs['pk'])
        return AlbumReviewComment.objects.filter(album_review_id=review)

    def perform_create(self, serializer):
        review = AlbumReview.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, album_review_id=review)


class AlbumReviewCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AlbumReviewComment.objects.all()
    serializer_class = AlbumReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = AlbumReviewComment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("Action forbidden! You're trying to delete someone else's comment!")

    def put(self, request, *args, **kwargs):
        comment = AlbumReviewComment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError("Action forbidden! You're trying to edit someone else's comment!")

class AlbumReviewLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = AlbumReviewLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        review = AlbumReview.objects.get(pk=self.kwargs['pk'])
        return AlbumReviewLike.objects.filter(user_id=user, album_review_id=review)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already liked this review!')
        user = self.request.user
        review = AlbumReview.objects.get(pk=self.kwargs['pk'])
        serializer.save(user_id=user, album_review_id=review)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You haven\'t liked this review before!')




