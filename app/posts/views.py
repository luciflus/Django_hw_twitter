from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import views, status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import authentication, permissions
from .permissions import PostPermission
from rest_framework import permissions

from .models import Tweet, StatusTweet, StatusType, Comment
from .serializers import TweetSerializer, StatusTweetSerializer, StatusTypeSerializer, CommentSerializer

class PostPagePagination(PageNumberPagination):
    page_size = 3 #elemente na str

class TweetViewSet(viewsets.ModelViewSet):
    """
    API for creation, geting, updating and deleting of tweets
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [PostPermission, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['text', ]
    search_fields = ['text', ]
    ordering_fields = ['updated_at', 'created_at']
    pagination_class = LimitOffsetPagination

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     #rint(queryset)
    #     text = self.request.query_params.get('text')
    #     if text:
    #         queryset = queryset.filter(text__icontains=text)
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def perform_update(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def perform_destroy(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(methods=['POST', 'GET'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def leave_status(self, request, pk=None):
       serializer = StatusTweetSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save(
               profile=request.user.profile,
               tweet=self.get_object()
           )
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [PostPermission, ]

    def get_queryset(self):
        #print(self.kwargs) ##prosmotret resultat
        return super().get_queryset().filter(tweet_id=self.kwargs.get('tweet_id'))

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            tweet_id=self.kwargs.get('tweet_id')
        )

class StatusTypeCreateListView(generics.ListCreateAPIView):
    queryset = StatusType.objects.all()
    serializer_class = StatusTypeSerializer



