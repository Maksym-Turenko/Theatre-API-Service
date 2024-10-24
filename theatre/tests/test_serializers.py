from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.test import APIRequestFactory
from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    TicketSerializer,
    ReservationSerializer,
    ReservationDetailSerializer,
)
from django.utils import timezone


class ActorSerializerTests(TestCase):

    def setUp(self):
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")

    def test_actor_serializer(self):
        serializer = ActorSerializer(self.actor)
        data = serializer.data
        self.assertEqual(data["first_name"], self.actor.first_name)
        self.assertEqual(data["last_name"], self.actor.last_name)
        self.assertEqual(data["full_name"], self.actor.full_name)


class GenreSerializerTests(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(name="Drama")

    def test_genre_serializer(self):
        serializer = GenreSerializer(self.genre)
        data = serializer.data
        self.assertEqual(data["name"], self.genre.name)


class PlaySerializerTests(TestCase):

    def setUp(self):
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.genre = Genre.objects.create(name="Drama")
        self.play = Play.objects.create(
            title="Test Play", description="A test play description"
        )
        self.play.actors.add(self.actor)
        self.play.genres.add(self.genre)

    def test_play_serializer(self):
        serializer = PlaySerializer(self.play)
        data = serializer.data
        self.assertEqual(data["title"], self.play.title)
        self.assertEqual(data["description"], self.play.description)
        self.assertEqual(data["actors"], [self.actor.id])
        self.assertEqual(data["genres"], [self.genre.id])

    def test_play_list_serializer(self):
        serializer = PlayListSerializer(self.play)
        data = serializer.data
        self.assertEqual(data["title"], self.play.title)
        self.assertEqual(data["description"], self.play.description)
        self.assertEqual(data["actors"][0], self.actor.full_name)
        self.assertEqual(data["genres"][0], self.genre.name)

    def test_play_detail_serializer(self):
        serializer = PlayDetailSerializer(self.play)
        data = serializer.data
        self.assertEqual(data["title"], self.play.title)
        self.assertEqual(data["description"], self.play.description)
        self.assertEqual(data["actors"][0]["full_name"], self.actor.full_name)
        self.assertEqual(data["genres"][0]["name"], self.genre.name)


class TheatreHallSerializerTests(TestCase):

    def setUp(self):
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_rows=10
        )

    def test_theatre_hall_serializer(self):
        serializer = TheatreHallSerializer(self.theatre_hall)
        data = serializer.data
        self.assertEqual(data["name"], self.theatre_hall.name)
        self.assertEqual(data["rows"], self.theatre_hall.rows)
        self.assertEqual(data["seats_in_rows"], self.theatre_hall.seats_in_rows)


class PerformanceSerializerTests(TestCase):

    def setUp(self):
        self.play = Play.objects.create(
            title="Test Play", description="A test play description"
        )
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_rows=10
        )
        self.show_time = timezone.now() + timedelta(days=31)
        self.performance = Performance.objects.create(
            play=self.play, theatre_hall=self.theatre_hall, show_time=self.show_time
        )

    def test_performance_serializer(self):
        serializer = PerformanceSerializer(self.performance)
        data = serializer.data
        self.assertEqual(data["play"], self.play.id)
        self.assertEqual(data["theatre_hall"], self.theatre_hall.id)
        show_time = self.show_time.isoformat().replace("+00:00", "Z")
        self.assertEqual(data["show_time"], show_time)

    def test_invalid_performance_show_time(self):
        invalid_show_time = timezone.now() + timedelta(days=29)
        performance = Performance(
            play=self.play, theatre_hall=self.theatre_hall, show_time=invalid_show_time
        )
        serializer = PerformanceSerializer(
            data={
                "play": self.play.id,
                "theatre_hall": self.theatre_hall.id,
                "show_time": invalid_show_time.isoformat(),
            }
        )
        with self.assertRaises(DRFValidationError):
            serializer.is_valid(raise_exception=True)


class TicketSerializerTests(TestCase):

    def setUp(self):
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
        self.ticket = Ticket.objects.create(row=1, seat=1, performance=self.performance)

    def test_ticket_serializer(self):
        serializer = TicketSerializer(self.ticket)
        data = serializer.data
        self.assertEqual(data["row"], self.ticket.row)
        self.assertEqual(data["seat"], self.ticket.seat)
        self.assertEqual(data["performance"], self.performance.id)

    def test_invalid_ticket(self):
        ticket_data = {"row": 11, "seat": 1, "performance": self.performance.id}
        serializer = TicketSerializer(data=ticket_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Row 11 does not exist in Test Hall.", serializer.errors["__all__"])


class ReservationSerializerTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
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
        self.ticket = Ticket.objects.create(row=1, seat=1, performance=self.performance)

    def test_reservation_serializer(self):
        reservation = Reservation.objects.create(user=self.user)
        self.ticket.reservation = reservation
        self.ticket.save()
        serializer = ReservationSerializer(instance=reservation)
        data = serializer.data
        self.assertEqual(data["play_title"], self.play.title)
        self.assertEqual(data["seat_info"], f"Row: {self.ticket.row}, Seat: {self.ticket.seat}")

    def test_invalid_reservation(self):
        reservation = Reservation.objects.create(user=self.user)
        self.ticket.reservation = reservation
        self.ticket.save()

        new_reservation_data = {"user": self.user.id, "ticket_id": self.ticket.id}

        factory = APIRequestFactory()
        request = factory.post('/api/reservations/', data=new_reservation_data)
        request.user = self.user
        serializer = ReservationSerializer(data=new_reservation_data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertIn('ticket_id', serializer.errors)


