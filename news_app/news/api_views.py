"""
API views for the News App.

This module provides REST API endpoints for interacting with articles.
It allows authenticated users to retrieve articles, create new articles,
update their own articles, and view articles from subscribed
journalists or publishers.
"""

from rest_framework import generics, status
from .models import Article, Publisher
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsJournalist, IsAuthorOrEditor
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from rest_framework import serializers


class ArticleListCreateAPI(generics.ListCreateAPIView):
    """
    API endpoint for listing approved articles and creating new ones.

    GET:
        Returns all approved articles.

    POST:
        Allows authenticated journalists to create a new article.
        Articles are created with approved=False and must be approved
        by an editor before becoming publicly visible.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        """
        Apply different permissions depending on request method.

        POST requests require the user to be an authenticated journalist.
        GET requests require the user to be authenticated.
        """
        if self.request.method == "POST":
            return [IsAuthenticated(), IsJournalist()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Return the queryset based on request type.

        GET requests return only approved articles.
        Other request types return all articles.
        """
        if self.request.method == "GET":
            return Article.objects.filter(approved=True)
        return Article.objects.all()

    def perform_create(self, serializer):
        """
        Save the article with the current user as the author
        and mark it as not approved.
        """
        serializer.save(author=self.request.user, approved=False)


class ArticleDetailUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific article.

    Access is restricted to authenticated users who are either
    the article's author or an editor.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrEditor]

    def perform_update(self, serializer):
        """
        Update the article and send a notification if the article
        has just been approved.
        """
        old_instance = self.get_object()
        instance = serializer.save()

        if not old_instance.approved and instance.approved:
            try:
                requests.post("http://127.0.0.1:8000/api/approved/", json={
                    "article": instance.title
                }, timeout=5)
            except requests.RequestException:
                pass


class SubscribedArticlesAPI(APIView):
    """
    API endpoint that returns approved articles from journalists
    or publishers that the authenticated user is subscribed to.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve approved articles written by journalists or publishers
        that the current user follows.
        """
        user = request.user
        articles = Article.objects.filter(
            approved=True,
            author__in=user.subscribed_journalists.all()
        ) | Article.objects.filter(
            approved=True,
            publisher__in=user.subscribed_publishers.all()
        )

        serializer = ArticleSerializer(articles.distinct(), many=True)
        return Response(serializer.data)


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Publisher model.
    """
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    Converts Article instances into JSON format and ensures
    that certain fields (author and approved status) are read-only.
    """

    author = serializers.ReadOnlyField(source='author.username')
    publisher = PublisherSerializer(read_only=True)
    approved = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author',
            'publisher', 'created_at', 'approved'
        ]


@api_view(['POST'])
def approved_article(request):
    """
    API endpoint used to log or acknowledge when an article
    has been approved by an editor.
    """
    article_title = request.data.get("article")
    if not article_title:
        return Response(
            {"error": "Missing 'article' field in request."},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response({
        "message": f"Article '{article_title}' has been approved and logged!"
    })
