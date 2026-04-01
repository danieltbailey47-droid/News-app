"""
URL routing for the News App.

This module defines all application routes including
authentication pages, article management views,
and REST API endpoints.
"""

from django.urls import path
from .views import (
    home, signup, login_view, logout_view, dashboard,
    create_article, approve_articles, article_list_view,
    subscribed_articles_view, toggle_subscribe_journalist, edit_article
)
from .api_views import (
    SubscribedArticlesAPI, approved_article,
    ArticleListCreateAPI, ArticleDetailUpdateDeleteAPI,
)

urlpatterns = [

    path('', home),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard),
    path('create-article/', create_article),
    path('approve-articles/', approve_articles),
    path('articles/', article_list_view),
    path('articles/subscribed/', subscribed_articles_view),
    path('toggle-subscribe/<int:journalist_id>/', toggle_subscribe_journalist,
         name='toggle_subscribe_journalist'),
    path('edit-article/<int:article_id>/', edit_article, name='edit_article'),


    path('api/articles/', ArticleListCreateAPI.as_view()),
    path('api/articles/<int:pk>/', ArticleDetailUpdateDeleteAPI.as_view()),
    path('api/articles/subscribed/', SubscribedArticlesAPI.as_view()),
    path('api/approved/', approved_article),
]
