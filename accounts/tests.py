from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class SignUpAndProfileTests(TestCase):
    def test_signup_creates_student_and_shows_success_message(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newstudent",
                "email": "student@example.com",
                "first_name": "New",
                "last_name": "Student",
                "course": "BSIT",
                "password1": "StrongPass!9274",
                "password2": "StrongPass!9274",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("login"))
        user = CustomUser.objects.get(username="newstudent")
        self.assertEqual(user.role, CustomUser.Role.STUDENT)
        self.assertTrue(user.check_password("StrongPass!9274"))
        self.assertContains(response, "Your account has been created")

    def test_profile_requires_login_and_updates_only_allowed_fields(self):
        profile_url = reverse("profile")
        response = self.client.get(profile_url)
        self.assertRedirects(response, f"{reverse('login')}?next={profile_url}")

        user = CustomUser.objects.create_user(
            username="profileuser",
            password="StrongPass!9274",
            role=CustomUser.Role.STUDENT,
            course="BSIT",
        )
        self.client.force_login(user)
        response = self.client.post(
            profile_url,
            {
                "username": "profileuser",
                "email": "updated@example.com",
                "first_name": "Updated",
                "last_name": "Student",
                "course": "BSCS",
                "role": CustomUser.Role.ADMIN,
            },
        )

        self.assertRedirects(response, profile_url)
        user.refresh_from_db()
        self.assertEqual(user.email, "updated@example.com")
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.course, "BSCS")
        self.assertEqual(user.role, CustomUser.Role.STUDENT)

    def test_profile_page_renders_with_csrf(self):
        user = CustomUser.objects.create_user(
            username="profileviewer",
            password="StrongPass!9274",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit your profile")
        self.assertContains(response, "csrfmiddlewaretoken")
