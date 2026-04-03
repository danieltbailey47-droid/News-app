"""
URL routing for the News App.

Defines application routes including authentication, article management,
publisher/editor workflows, and REST API endpoints.
"""

from django.urls import path
from .views import (
    home, signup, login_view, logout_view, dashboard,
    create_article, approve_articles, article_list_view,
    subscribed_articles_view, toggle_subscribe_journalist,
    edit_article, publisher_dashboard
)
from .api_views import (
    SubscribedArticlesAPI, approved_article,
    ArticleListCreateAPI, ArticleDetailUpdateDeleteAPI,
)

urlpatterns = [
    # Authentication
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),

    # User Dashboards
    path('dashboard/', dashboard, name='dashboard'),
    path('publisher_dashboard/', publisher_dashboard,
         name='publisher_dashboard'),

    # Article Management
    path('create-article/', create_article, name='create_article'),
    path('edit-article/<int:article_id>/', edit_article, name='edit_article'),
    path('approve-articles/', approve_articles, name='approve_articles'),

    # Article Viewing
    path('articles/', article_list_view, name='article_list'),
    path('articles/subscribed/', subscribed_articles_view,
         name='subscribed_articles'),

    # Subscriptions
    path('toggle-subscribe/<int:journalist_id>/', toggle_subscribe_journalist,
         name='toggle_subscribe_journalist'),

    # REST API Endpoints
    path('api/articles/', ArticleListCreateAPI.as_view(),
         name='api_article_list_create'),
    path('api/articles/<int:pk>/', ArticleDetailUpdateDeleteAPI.as_view(),
         name='api_article_detail'),
    path('api/articles/subscribed/', SubscribedArticlesAPI.as_view(),
         name='api_subscribed_articles'),
    path('api/approved/', approved_article, name='api_approved_articles'),
]
