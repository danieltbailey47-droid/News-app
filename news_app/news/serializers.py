"""
Serializers for the News App.

This module provides serializers for converting Django models
into JSON for the REST API, and for validating incoming
data when creating or updating objects via the API.
"""

from rest_framework import serializers
from .models import Article, Publisher, Newsletter, CustomUser


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Publisher model.

    Converts Publisher instances to JSON and validates
    incoming data for creating or updating publishers.
    """

    class Meta:
        model = Publisher
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    Includes nested publisher information and read-only
    author username. Used for listing, retrieving, creating,
    and updating articles via the API.
    """

    author = serializers.ReadOnlyField(source='author.username')
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author',
            'publisher', 'created_at', 'approved'
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Newsletter model.

    Serializes newsletter details including related articles
    and author information.
    """

    class Meta:
        model = Newsletter
        fields = [
            'id', 'title', 'description',
            'created_at', 'author', 'articles'
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    Includes basic user information and lists of subscribed
    publishers and journalists.
    """

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'role',
            'subscribed_publishers',
            'subscribed_journalists'
        ]
