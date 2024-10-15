from datetime import timedelta

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from user_config.models import User


class Actor(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["first_name", "last_name"]


class Genre(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Play(models.Model):
    title = models.CharField(max_length=63, unique=True)
    description = models.TextField(blank=True)
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="plays")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=63, unique=True)
    rows = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    seats_in_rows = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def clean(self):
        super().clean()
        if self.show_time < timezone.now() + timedelta(days=30):
            raise ValidationError(
                "The Performance date must be at least one month from today."
            )

    def __str__(self):
        return f"{self.play.title} - " f'{self.show_time.strftime("%Y-%m-%d %H:%M")}'

    class Meta:
        ordering = ["-show_time"]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Reserved by {self.user.email} on {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    seat = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    performance = models.ForeignKey(
        Performance,
        on_delete=models.PROTECT,
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="tickets",
    )

    def clean(self):
        super().clean()
        theatre_hall = self.performance.theatre_hall
        if self.row > theatre_hall.rows:
            raise ValidationError(
                f"Row {self.row} does not exist in {theatre_hall.name}."
            )
        if self.seat > theatre_hall.seats_in_rows:
            raise ValidationError(
                f"Seat {self.seat} does not exist in "
                f"row {self.row} of {theatre_hall.name}."
            )

    def __str__(self):
        return (
            f"Performance: {self.performance}, "
            f"row: {self.row}, "
            f"seat: {self.seat}, "
            f"Hall: {self.performance.theatre_hall.name}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "performance"], name="unique_ticket"
            )
        ]
