from django.urls import path,include
from . views import (
    BandList, AlbumList, SongList, AlbumReviewList, AlbumReviewCommentList,
    BandDetail, AlbumDetail, SongDetail, AlbumReviewDetail, AlbumReviewCommentDetail, AlbumReviewLikeCreate
)

urlpatterns = [
    path('bands/', BandList.as_view()),
    path('albums/', AlbumList.as_view()),
    path('songs/', SongList.as_view()),
    path('reviews/', AlbumReviewList.as_view()),
    path('bands/<int:pk>', BandDetail.as_view()),
    path('albums/<int:pk>', AlbumDetail.as_view()),
    path('songs/<int:pk>', SongDetail.as_view()),
    path('reviews/<int:pk>', AlbumReviewDetail.as_view()),
    path('reviews/<int:pk>/comments', AlbumReviewCommentList.as_view()),
    path('comments/<int:pk>', AlbumReviewCommentDetail.as_view()),
    path('reviews/<int:pk>/like', AlbumReviewLikeCreate.as_view()),
]
