from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Article

User = get_user_model()


class UserModelTest(TestCase):

    def test_create_user_with_role(self):
        user = User.objects.create_user(
            username="testuser",
            password="password123",
            role="journalist"
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "journalist")


class LoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            role="reader"
        )

    def test_login(self):
        login = self.client.login(
            username="testuser",
            password="password123"
        )

        self.assertTrue(login)


class ArticleTest(TestCase):

    def setUp(self):
        self.journalist = User.objects.create_user(
            username="journalist1",
            password="password123",
            role="journalist"
        )

    def test_journalist_can_create_article(self):

        self.client.login(username="journalist1", password="password123")

        response = self.client.post("/create-article/", {
            "title": "Test Article",
            "content": "This is a test article."
        })

        self.assertEqual(response.status_code, 302)  # redirect to dashboard
        self.assertEqual(Article.objects.count(), 1)


class ApprovalTest(TestCase):

    def setUp(self):

        self.editor = User.objects.create_user(
            username="editor1",
            password="password123",
            role="editor"
        )

        self.journalist = User.objects.create_user(
            username="journalist1",
            password="password123",
            role="journalist"
        )

        self.article = Article.objects.create(
            title="Pending Article",
            content="Needs approval",
            author=self.journalist,
            approved=False
        )

    def test_editor_can_approve_article(self):

        self.client.login(username="editor1", password="password123")

        response = self.client.post("/approve-articles/", {
            "article_id": self.article.id
        })

        self.article.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.article.approved)


class SubscriptionTest(TestCase):

    def setUp(self):

        self.reader = User.objects.create_user(
            username="reader1",
            password="password123",
            role="reader"
        )

        self.journalist = User.objects.create_user(
            username="journalist1",
            password="password123",
            role="journalist"
        )

    def test_subscribe_to_journalist(self):

        self.reader.subscribed_journalists.add(self.journalist)

        self.assertIn(
            self.journalist,
            self.reader.subscribed_journalists.all()
        )