from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="password123"
        )
        self.client.force_login(self.admin_user)

        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.genre = Genre.objects.create(name="Drama")
        self.play = Play.objects.create(
            title="Test Play", description="A test play description"
        )
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_rows=10
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time=timezone.now() + timedelta(days=31),
        )
        self.reservation = Reservation.objects.create(user=self.admin_user)
        self.ticket = Ticket.objects.create(
            row=1, seat=1, performance=self.performance, reservation=self.reservation
        )

    def test_actor_admin(self):
        url = reverse("admin:theatre_actor_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_genre_admin(self):
        url = reverse("admin:theatre_genre_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_play_admin(self):
        url = reverse("admin:theatre_play_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_theatre_hall_admin(self):
        url = reverse("admin:theatre_theatrehall_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_performance_admin(self):
        url = reverse("admin:theatre_performance_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_reservation_admin(self):
        url = reverse("admin:theatre_reservation_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_ticket_admin(self):
        url = reverse("admin:theatre_ticket_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
