from django.contrib import admin
from django.db import models

from theatre.custom_mixins import (
    UserInfoMixin,
    PlayInfoMixin,
    TheatreHallInfoMixin,
)
from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ["id", "first_name", "last_name"]
    list_display = ["id", "full_name"]
    list_filter = ["first_name", "last_name"]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search_term)
                | models.Q(last_name__icontains=search_term)
            )
        return queryset, use_distinct


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]
    list_display = ["id", "name"]


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    search_fields = ["id", "title"]
    list_display = ["id", "title", "description", "get_actors", "get_genres"]
    list_filter = ["title", "actors", "genres"]

    def get_actors(self, obj):
        actors = obj.actors.all()
        return (
            ", ".join([actor.full_name for actor in actors])
            if actors.exists()
            else "No actors"
        )

    def get_genres(self, obj):
        genres = obj.genres.all()
        return (
            ", ".join([genre.name for genre in genres])
            if genres.exists()
            else "No genres"
        )

    get_actors.short_description = "Actors"
    get_genres.short_description = "Genres"


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]
    list_display = ["id", "name", "rows", "seats_in_rows"]
    list_filter = ["name", "rows", "seats_in_rows"]


@admin.register(Performance)
class PerformanceAdmin(PlayInfoMixin, TheatreHallInfoMixin, admin.ModelAdmin):
    search_fields = ["id", "play__title", "theatre_hall__name", "show_time"]
    list_display = ["id", "get_play_title", "get_theatre_hall_name", "show_time"]
    list_filter = ["play", "theatre_hall", "show_time"]


@admin.register(Reservation)
class ReservationAdmin(UserInfoMixin, admin.ModelAdmin):
    search_fields = ["id", "created_at", "user__username", "user__email"]
    list_display = ["id", "created_at", "get_user_username", "get_user_email"]


@admin.register(Ticket)
class TicketAdmin(UserInfoMixin, PlayInfoMixin, admin.ModelAdmin):
    search_fields = [
        "id",
        "performance__play__title",
        "reservation__user__username",
        "reservation__user__email",
    ]
    list_display = [
        "id",
        "get_play_title",
        "get_user_username",
        "get_user_email",
    ]
    list_filter = [
        "performance__play__title",
        "reservation__user__username",
        "reservation__user__email",
        "row",
        "seat",
        "performance",
    ]
