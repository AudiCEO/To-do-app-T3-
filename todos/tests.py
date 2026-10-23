from django.test import TestCase
from django.urls import reverse
from .models import Task


class TodoTests(TestCase):
    def test_insert_task(self):
        r = self.client.post(reverse("home"), {"title": "Buy milk", "notes": "2%", "due_date": ""})
        self.assertRedirects(r, reverse("home"))
        self.assertEqual(Task.objects.count(), 1)
        self.assertContains(self.client.get(reverse("home")), "Buy milk")

    def test_empty_title_rejected(self):
        self.client.post(reverse("home"), {"title": "", "notes": ""})
        self.assertEqual(Task.objects.count(), 0)

    def test_search_finds_title_and_notes_case_insensitive(self):
        Task.objects.create(title="Buy milk")
        Task.objects.create(title="Study", notes="read chapter on MILK pasteurization")
        Task.objects.create(title="Call mom")
        r = self.client.get(reverse("search"), {"q": "milk"})
        self.assertEqual(len(r.context["results"]), 2)

    def test_search_no_match(self):
        Task.objects.create(title="Buy milk")
        r = self.client.get(reverse("search"), {"q": "zebra"})
        self.assertContains(r, "0 results")

    def test_toggle_and_delete(self):
        t = Task.objects.create(title="x")
        self.client.post(reverse("toggle", args=[t.pk]))
        t.refresh_from_db()
        self.assertTrue(t.done)
        self.client.post(reverse("delete", args=[t.pk]))
        self.assertEqual(Task.objects.count(), 0)
