from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)
from django.utils import timezone
from datetime import timedelta


class ViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.genre = Genre.objects.create(name="Drama")
        self.play = Play.objects.create(
            title="Test Play", description="A test play description"
        )
        self.play.actors.add(self.actor)
        self.play.genres.add(self.genre)

        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_rows=10
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time=timezone.now() + timedelta(days=31),
        )

        self.reservation = Reservation.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=1, seat=1, performance=self.performance, reservation=self.reservation
        )

    def test_actor_view_set(self):
        response = self.client.get(reverse("actor-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_view_set(self):
        response = self.client.get(reverse("genre-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_play_view_set(self):
        response = self.client.get(reverse("play-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_theatre_hall_view_set(self):
        response = self.client.get(reverse("theatrehall-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_performance_view_set(self):
        response = self.client.get(reverse("performance-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_view_set(self):
        response = self.client.get(reverse("reservation-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ticket_view_set(self):
        response = self.client.get(reverse("ticket-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actor_view_set_filtering(self):
        response = self.client.get(reverse("actor-list") + "?name=John")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_genre_view_set_filtering(self):
        response = self.client.get(reverse("genre-list") + "?name=Drama")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_play_view_set_filtering_by_actor(self):
        response = self.client.get(reverse("play-list") + "?actor_name=John Doe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_play_view_set_filtering_by_title(self):
        response = self.client.get(reverse("play-list") + "?play_title=Test Play")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_play_view_set_filtering_by_genre(self):
        response = self.client.get(reverse("play-list") + "?genre_name=Drama")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_performance_view_set_filtering_by_play_title(self):
        response = self.client.get(
            reverse("performance-list") + "?play_title=Test Play"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_performance_view_set_filtering_by_actor(self):
        response = self.client.get(reverse("performance-list") + "?actor_name=John Doe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_performance_view_set_filtering_by_hall_name(self):
        response = self.client.get(reverse("performance-list") + "?hall_name=Test Hall")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_reservation_view_set_filtering_by_username(self):
        response = self.client.get(reverse("reservation-list") + "?username=testuser")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_ticket_view_set_filtering_by_hall_name(self):
        response = self.client.get(reverse("ticket-list") + "?hall_name=Test Hall")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_ticket_view_set_filtering_by_performance_title(self):
        response = self.client.get(
            reverse("ticket-list") + "?performance_title=Test Play"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_ticket_view_set_filtering_by_username(self):
        response = self.client.get(reverse("ticket-list") + "?username=testuser")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
