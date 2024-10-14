from rest_framework import serializers

from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class PlaySerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(many=True, queryset=Actor.objects.all())
    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())

    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class PlayListSerializer(serializers.ModelSerializer):
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class PlayDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_rows"]


class PerformanceSerializer(serializers.ModelSerializer):
    play = serializers.PrimaryKeyRelatedField(queryset=Play.objects.all())
    theatre_hall = serializers.PrimaryKeyRelatedField(
        queryset=TheatreHall.objects.all()
    )

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]

    def validate(self, data):
        performance = Performance(**data)
        performance.clean()
        return data


class PerformanceListSerializer(serializers.ModelSerializer):
    play = PlayListSerializer(read_only=True)
    theatre_hall = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]

    def get_theatre_hall(self, obj):
        return {
            "name": obj.theatre_hall.name,
            "rows": obj.theatre_hall.rows,
            "seats_in_rows": obj.theatre_hall.seats_in_rows,
        }


class PerformanceDetailSerializer(serializers.ModelSerializer):
    play = PlayDetailSerializer()
    theatre_hall = TheatreHallSerializer()

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]

    def validate_ticket_id(self, value):
        if value.reservation is not None:
            raise serializers.ValidationError("This ticket is already reserved.")
        return value

    def create(self, validated_data):
        ticket = validated_data["ticket"]
        reservation = Reservation.objects.create(**validated_data)
        ticket.reservation = reservation
        ticket.save()
        return reservation


class TicketSerializer(serializers.ModelSerializer):
    performance = serializers.PrimaryKeyRelatedField(queryset=Performance.objects.all())

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance"]

    def validate(self, data):
        performance = data["performance"]
        theatre_hall = performance.theatre_hall
        existing_tickets = Ticket.objects.filter(performance=performance).count()

        if existing_tickets >= (theatre_hall.rows * theatre_hall.seats_in_rows):
            raise serializers.ValidationError(
                "The number of tickets exceeds the hall capacity."
            )

        return data


class TicketListSerializer(serializers.ModelSerializer):
    performance = serializers.SlugRelatedField(read_only=True, slug_field="play__title")
    reservation_username = serializers.SerializerMethodField()
    reservation_email = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "row",
            "seat",
            "performance",
            "reservation_username",
            "reservation_email",
        ]

    def get_reservation_username(self, obj):
        if obj.reservation:
            return obj.reservation.user.username
        return None

    def get_reservation_email(self, obj):
        if obj.reservation:
            return obj.reservation.user.email
        return None


class TicketDetailSerializer(TicketSerializer):
    performance = serializers.SerializerMethodField()
    reservation = serializers.SerializerMethodField()

    class Meta(TicketSerializer.Meta):
        fields = ["row", "seat", "performance", "reservation"]

    def get_performance(self, obj):
        return {
            "title": obj.performance.play.title,
            "actors": [actor.full_name for actor in obj.performance.play.actors.all()],
            "genres": [genre.name for genre in obj.performance.play.genres.all()],
            "theatre_hall": {
                "name": obj.performance.theatre_hall.name,
                "rows": obj.performance.theatre_hall.rows,
                "seats_in_rows": obj.performance.theatre_hall.seats_in_rows,
            },
            "show_time": obj.performance.show_time,
        }

    def get_reservation(self, obj):
        if obj.reservation:
            return {
                "username": obj.reservation.user.username,
                "email": obj.reservation.user.email,
            }
        return None


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ticket_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(), write_only=True
    )
    play_title = serializers.SerializerMethodField()
    seat_info = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "play_title", "seat_info", "ticket_id", "user"]

    def get_play_title(self, obj):
        ticket = obj.tickets.first()
        if ticket:
            return ticket.performance.play.title
        return None

    def get_seat_info(self, obj):
        ticket = obj.tickets.first()
        if ticket:
            return f"Row: {ticket.row}, Seat: {ticket.seat}"
        return None

    def validate_ticket_id(self, value):
        if value.reservation is not None:
            raise serializers.ValidationError("This ticket is already reserved.")
        return value

    def create(self, validated_data):
        user = validated_data["user"]
        ticket = validated_data["ticket_id"]

        reservation = Reservation.objects.create(user=user)

        ticket.reservation = reservation
        ticket.save()

        return reservation


class ReservationDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tickets = TicketDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user", "tickets"]
