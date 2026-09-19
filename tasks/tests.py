from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="sajid", password="testpass123")

    def test_task_creation(self):
        task = Task.objects.create(
            user=self.user, title="Learn Django", description="Study Django models"
        )
        self.assertEqual(task.title, "Learn Django")
        self.assertFalse(task.completed)

    def test_task_belongs_to_user(self):
        task = Task.objects.create(user=self.user, title="My Task")
        self.assertEqual(task.user, self.user)


class AuthAndPagesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="sajid", password="testpass123")

    def test_anonymous_home_redirects_to_login_instead_of_crashing(self):
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_login_and_register_pages_load_and_link_css(self):
        for name in ("login", "register"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "css/style.css")
            self.assertContains(response, 'class="auth-card"')

    def test_page_title_block_is_used(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Dashboard | TaskFlow")

    def test_navbar_has_logout_form_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'action="/accounts/logout/"')

    def test_logout_works_via_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))


class RegisterTest(TestCase):

    def test_weak_password_is_rejected(self):
        response = self.client.post(
            reverse("register"),
            {"username": "newbie", "email": "n@example.com", "password": "1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newbie").exists())

    def test_valid_registration_creates_user_and_hashes_password(self):
        response = self.client.post(
            reverse("register"),
            {"username": "newbie", "email": "n@example.com", "password": "Str0ng-pass-987"},
        )
        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="newbie")
        self.assertNotEqual(user.password, "Str0ng-pass-987")
        self.assertTrue(user.check_password("Str0ng-pass-987"))


class TaskViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="sajid", password="testpass123")
        self.other = User.objects.create_user(username="other", password="testpass123")
        self.client.force_login(self.user)

    def test_create_task(self):
        response = self.client.post(
            reverse("create_task"), {"title": "Write tests", "priority": "high"}
        )
        self.assertRedirects(response, reverse("home"))
        task = Task.objects.get(title="Write tests")
        self.assertEqual(task.user, self.user)

    def test_stats_ignore_filters(self):
        Task.objects.create(user=self.user, title="a", priority="high", completed=True)
        Task.objects.create(user=self.user, title="b", priority="low")
        Task.objects.create(user=self.other, title="not mine", priority="high")

        response = self.client.get(reverse("home"), {"status": "completed"})
        self.assertEqual(len(response.context["tasks"]), 1)
        self.assertEqual(response.context["total_tasks"], 2)
        self.assertEqual(response.context["completed_tasks"], 1)
        self.assertEqual(response.context["pending_tasks"], 1)
        self.assertEqual(response.context["high_priority"], 1)

    def test_pagination_links_keep_filters(self):
        for i in range(12):
            Task.objects.create(user=self.user, title=f"Task {i}", priority="low")

        response = self.client.get(reverse("home"), {"priority": "low"})
        self.assertContains(response, "priority=low")
        self.assertContains(response, "page=2")

    def test_toggle_requires_post(self):
        task = Task.objects.create(user=self.user, title="t")
        url = reverse("toggle_task", args=[task.id])

        self.assertEqual(self.client.get(url).status_code, 405)
        task.refresh_from_db()
        self.assertFalse(task.completed)

        self.client.post(url)
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_delete_requires_post(self):
        task = Task.objects.create(user=self.user, title="t")
        url = reverse("delete_task", args=[task.id])

        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        self.client.post(url)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_cannot_touch_another_users_task(self):
        task = Task.objects.create(user=self.other, title="private")
        self.assertEqual(self.client.post(reverse("delete_task", args=[task.id])).status_code, 404)
        self.assertEqual(self.client.post(reverse("toggle_task", args=[task.id])).status_code, 404)
        self.assertTrue(Task.objects.filter(id=task.id).exists())
