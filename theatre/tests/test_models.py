from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from theatre.models import (
    Performance,
    Play,
    TheatreHall,
    Ticket,
    Reservation,
)


class PerformanceModelTests(TestCase):

    def setUp(self):
        self.play = Play.objects.create(
            title="Test Play", description="A test play description"
        )
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_rows=10
        )

    def test_performance_creation(self):
        show_time = timezone.now() + timedelta(days=31)
        performance = Performance(
            play=self.play, theatre_hall=self.theatre_hall, show_time=show_time
        )
        performance.clean()  # should not raise ValidationError
        performance.save()
        self.assertEqual(Performance.objects.count(), 1)

    def test_performance_creation_with_invalid_show_time(self):
        show_time = timezone.now() + timedelta(days=29)
        performance = Performance(
            play=self.play, theatre_hall=self.theatre_hall, show_time=show_time
        )
        with self.assertRaises(ValidationError):
            performance.clean()


class TicketModelTests(TestCase):

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

    def test_ticket_creation(self):
        ticket = Ticket(row=1, seat=1, performance=self.performance)
        try:
            ticket.clean()  # should not raise ValidationError
            ticket.save()
        except ValidationError:
            self.fail("Ticket creation raised ValidationError unexpectedly!")

    def test_ticket_creation_with_invalid_row(self):
        ticket = Ticket(row=11, seat=1, performance=self.performance)
        with self.assertRaises(ValidationError):
            ticket.clean()

    def test_ticket_creation_with_invalid_seat(self):
        ticket = Ticket(row=1, seat=11, performance=self.performance)
        with self.assertRaises(ValidationError):
            ticket.clean()

    def test_ticket_reservation(self):
        reservation = Reservation.objects.create(user=self.user)
        ticket = Ticket.objects.create(
            row=1, seat=1, performance=self.performance, reservation=reservation
        )
        self.assertEqual(ticket.reservation, reservation)
        self.assertEqual(reservation.user, self.user)
