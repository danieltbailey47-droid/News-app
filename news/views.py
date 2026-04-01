"""
Main web views for the News App.

This module handles user authentication, dashboards, article creation,
editing, approvals, subscriptions, and article browsing for the web
interface of the application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Article, Publisher
from django.core.mail import send_mail
from .forms import CustomUserCreationForm


def home(request):
    """
    Render the home page of the News App.
    """
    return render(request, "home.html")


def signup(request):
    """
    Handle user registration.

    Displays a registration form and creates a new user
    when valid data is submitted.
    """

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    """
    Authenticate a user and log them into the system.

    If credentials are invalid, an error message is shown.
    """

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/dashboard')
        else:
            return render(request, "registration/login.html", {
                "error": "Invalid credentials"
            })

    return render(request, 'registration/login.html')


@login_required
def dashboard(request):
    """
    Display the user dashboard.

    The dashboard content may vary depending on the
    role of the logged-in user.
    """

    return render(request, "registration/dashboard.html", {
        "role": request.user.role
    })


@login_required
def create_article(request):
    """
    Allow journalists to create new articles.

    Articles are created with approved=False and must
    be approved by an editor before publication.
    """

    if request.user.role != "journalist":
        return render(request, "not_authorized.html")

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        publisher_id = request.POST.get("publisher")

        if not title or not content:
            return render(request, "articles/create_article.html", {
                "error": "Title and content are required"
            })

        publisher = None
        if publisher_id:
            publisher = Publisher.objects.get(id=publisher_id)

        Article.objects.create(
            title=title,
            content=content,
            author=request.user,
            publisher=publisher,
            approved=False
        )

        return redirect("/dashboard")

    publishers = Publisher.objects.all()

    return render(request, "articles/create_article.html", {
        "publishers": publishers
    })


@login_required
def approve_articles(request):
    """
    Allow editors to review pending articles.

    Editors can approve or decline submitted articles.
    Approved articles trigger email notifications to
    subscribers.
    """

    if request.user.role != "editor":
        return render(request, "not_authorized.html")

    articles = Article.objects.filter(approved=False)

    if request.method == "POST":
        article_id = request.POST.get("article_id")
        action = request.POST.get("action")

        article = get_object_or_404(Article, id=article_id)

        if action == "approve":
            article.approved = True
            article.save()

            journalist_subscribers = article.author.subscribed_journalists.all()

            publisher_subscribers = []
            if article.publisher:
                publisher_subscribers = article.publisher.subscribers.all()

            subscribers = list(journalist_subscribers) + list(publisher_subscribers)

            emails = [user.email for user in subscribers if user.email]

            if emails:
                send_mail(
                    "New Article Published",
                    f"{article.title} has been approved and published.",
                    "admin@newsapp.com",
                    emails,
                    fail_silently=True,
                )

        elif action == "decline":
            article.delete()

        return redirect("/approve-articles/")

    return render(request, "articles/approve_articles.html", {
        "articles": articles
    })


def logout_view(request):
    """
    Log the user out and redirect to the home page.
    """

    logout(request)
    return redirect("/")


@login_required
def article_list_view(request):
    """
    Display a list of all approved articles.
    """

    articles = Article.objects.filter(approved=True)

    return render(request, "articles/article_list.html", {
        "articles": articles,
        "role": request.user.role
    })


@login_required
def subscribed_articles_view(request):
    """
    Display articles from journalists and publishers
    that the user is subscribed to.
    """

    user = request.user

    articles = Article.objects.filter(
        approved=True,
        publisher__in=user.subscribed_publishers.all()
    ) | Article.objects.filter(
        approved=True,
        author__in=user.subscribed_journalists.all()
    )

    return render(request, "articles/subscribed_articles.html", {
        "articles": articles.distinct(),
        "role": user.role
    })


@login_required
def toggle_subscribe_journalist(request, journalist_id):
    """
    Subscribe or unsubscribe the current user
    from a specific journalist.
    """

    journalist = get_object_or_404(CustomUser, id=journalist_id)

    if journalist != request.user:

        if journalist in request.user.subscribed_journalists.all():
            request.user.subscribed_journalists.remove(journalist)
        else:
            request.user.subscribed_journalists.add(journalist)

    return redirect("/articles/")


@login_required
def edit_article(request, article_id):
    """
    Allow the author of an article to edit its title
    and content.
    """

    article = get_object_or_404(Article, id=article_id)

    if request.user != article.author:
        return render(request, "not_authorized.html")

    if request.method == "POST":
        article.title = request.POST["title"]
        article.content = request.POST["content"]
        article.save()
        return redirect("/dashboard")

    return render(request, "articles/edit_article.html", {"article": article})
