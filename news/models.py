"""
Database models for the News App.

Defines the core data structures used in the application,
including users, publishers, articles, and newsletters.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLE_Choice = (
    ('reader', 'Reader'),
    ('editor', 'Editor'),
    ('journalist', 'Journalist'),
    ('publisher', 'Publisher')
)


class Publisher(models.Model):
    """
    Represents a news publisher.

    Articles can optionally be associated with a publisher,
    and users can subscribe to publishers to receive their articles.
    """
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField('CustomUser', related_name='publishers')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Users can have different roles such as reader, editor,
    or journalist. Readers can subscribe to publishers or
    individual journalists to receive article updates.
    """

    email = models.EmailField(unique=True, blank=False)

    role = models.CharField(max_length=20,
                            choices=ROLE_Choice, default='reader')

    subscribed_publishers = models.ManyToManyField(
        Publisher, blank=True, related_name="subscribers"
    )
    subscribed_journalists = models.ManyToManyField(
        "self", blank=True, symmetrical=False
    )


class Article(models.Model):
    """
    Represents a news article written by a journalist.

    Articles may belong to a publisher and must be approved
    by an editor before becoming visible to readers.
    """

    title = models.CharField(max_length=225)
    content = models.TextField()

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    publisher = models.ForeignKey(
        Publisher,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.publisher is None:
            self.approved = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """
    Represents a newsletter containing a collection of articles.

    Newsletters are created by a user and can include multiple
    articles.
    """

    title = models.CharField(max_length=225)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.title
