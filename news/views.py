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
from django.db import IntegrityError


def home(request):
    """
    Render the home page of the News App.
    """
    return render(request, "home.html")


def signup(request):
    """
    User registration with:
    - Publisher registration
    - Editors/Journalists associated with publishers
    - Auto login after registration
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                role = form.cleaned_data.get("role")
                if role in ["editor", "journalist"]:
                    user.publisher = form.cleaned_data.get("publisher")
                user.save()
                login(request, user)
                return redirect("/dashboard")
            except IntegrityError:
                return render(request, "registration/signup.html", {
                    "form": form,
                    "error": "A user with this email or username already exists."
                })
        else:
            return render(request, "registration/signup.html", {
                "form": form,
                "error": "Please correct the errors below."
            })
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

    Articles with no publisher are auto-approved.
    Articles with a publisher require editor approval.
    """

    if request.user.role != "journalist":
        return render(request, "not_authorized.html")

    publishers = Publisher.objects.filter(journalists=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        publisher_id = request.POST.get("publisher")

        if not title or not content:
            return render(request, "articles/create_article.html", {
                "error": "Title and content are required",
                "publishers": publishers
            })

        publisher = get_object_or_404(Publisher, id=publisher_id) if publisher_id else None
        approved = False if publisher else True

        Article.objects.create(
            title=title,
            content=content,
            author=request.user,
            publisher=publisher,
            approved=approved
        )

        return redirect("/dashboard")

    return render(request, "articles/create_article.html", {
        "publishers": publishers
    })


@login_required
def approve_articles(request):
    """
    Allows editors to approve or reject articles.
    Only for articles from their associated publisher.
    """
    if request.user.role != "editor":
        return render(request, "not_authorized.html")

    publisher = request.user.publisher
    pending_articles = Article.objects.filter(publisher=publisher, approved=False)

    if request.method == "POST":
        action = request.POST.get("action")
        article_id = request.POST.get("article_id")
        article = Article.objects.get(id=article_id, publisher=publisher)

        if action == "approve":
            article.approved = True
        elif action == "decline":
            article.approved = False
        article.save()
        return redirect("/approve_articles")

    return render(request, "articles/approve_articles.html", {"articles": pending_articles})


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


@login_required
def publisher_dashboard(request):
    """
    Publisher dashboard:
    - Shows pending articles for editors
    - Shows associated editors and journalists
    """

    if request.user.role != "publisher":
        return render(request, "not_authorized.html")

    publisher = Publisher.objects.get(id=request.user.id)
    editors = CustomUser.objects.filter(role="editor", publisher=publisher)
    journalists = CustomUser.objects.filter(role="journalist", publisher=publisher)
    articles = Article.objects.filter(publisher=publisher, approved=False)

    context = {
        "publisher": publisher,
        "editors": editors,
        "journalists": journalists,
        "articles": articles,
    }
    return render(request, "publisher/dashboard.html", context)
