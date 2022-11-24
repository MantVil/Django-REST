from django.shortcuts import render
from rest_framework import generics
from . import models, serializers
# Create your views here.

class PostList(generics.ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer