from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter

from theatre.permissions import IsAdminOrReadOnly
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
    TheatreHallSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
    TicketListSerializer,
    PlayDetailSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    TicketDetailSerializer,
    ReservationDetailSerializer,
)


@extend_schema(tags=["Actors"])
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")

        if name:
            names = name.split()
            if len(names) == 2:
                queryset = queryset.filter(
                    Q(first_name__icontains=names[0]) & Q(last_name__icontains=names[1])
                ).distinct()
            else:
                queryset = queryset.filter(
                    Q(first_name__icontains=name) | Q(last_name__icontains=name)
                ).distinct()

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter("name", str, description="Filter actors by full name")
        ]
    )
    @extend_schema(
        parameters=[OpenApiParameter("name", str, description="Filter actors by name")],
        responses={200: ActorSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Retrieve actor by ID", responses={200: ActorSerializer})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Genres"])
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


@extend_schema(tags=["Plays"])
class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("actors", "genres")
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        elif self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        actor_name = self.request.query_params.get("actor_name")
        play_title = self.request.query_params.get("play_title")
        genre_name = self.request.query_params.get("genre_name")

        if actor_name:
            names = actor_name.split()
            if len(names) == 2:
                queryset = queryset.filter(
                    Q(actors__first_name__icontains=names[0])
                    & Q(actors__last_name__icontains=names[1])
                ).distinct()
            else:
                queryset = queryset.filter(
                    Q(actors__first_name__icontains=actor_name)
                    | Q(actors__last_name__icontains=actor_name)
                ).distinct()

        if play_title:
            queryset = queryset.filter(title__icontains=play_title)

        if genre_name:
            queryset = queryset.filter(genres__name__icontains=genre_name)

        return queryset

    @extend_schema(
        responses={200: PlayListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={200: PlayDetailSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Theatre Halls"])
class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(responses={200: TheatreHallSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(responses={200: TheatreHallSerializer})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Performances"])
class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall").prefetch_related("play__actors")
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        elif self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        play_title = self.request.query_params.get("play_title")
        actor_name = self.request.query_params.get("actor_name")
        hall_name = self.request.query_params.get("hall_name")

        if play_title:
            queryset = queryset.filter(play__title__icontains=play_title)

        if actor_name:
            names = actor_name.split()
            if len(names) == 2:
                queryset = queryset.filter(
                    Q(play__actors__first_name__icontains=names[0])
                    & Q(play__actors__last_name__icontains=names[1])
                ).distinct()
            else:
                queryset = queryset.filter(
                    Q(play__actors__first_name__icontains=actor_name)
                    | Q(play__actors__last_name__icontains=actor_name)
                    | Q(play__actors__full_name__icontains=actor_name)
                ).distinct()

        if hall_name:
            queryset = queryset.filter(theatre_hall__name__icontains=hall_name)
        return queryset

    @extend_schema(
        responses={200: PerformanceListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={200: PerformanceDetailSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Reservations"])
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("user")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationSerializer
        if self.action == "retrieve":
            return ReservationDetailSerializer
        return ReservationSerializer

    @extend_schema(responses={201: ReservationSerializer})
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(user__username__icontains=username)

        return queryset


@extend_schema(tags=["Tickets"])
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        "performance", "performance__theatre_hall", "reservation"
    )
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketDetailSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        hall_name = self.request.query_params.get("hall_name")
        performance_title = self.request.query_params.get("performance_title")
        username = self.request.query_params.get("username")

        if hall_name:
            queryset = queryset.filter(performance__theatre_hall__name__icontains=hall_name)

        if performance_title:
            queryset = queryset.filter(performance__play__title__icontains=performance_title)

        if username:
            queryset = queryset.filter(reservation__user__username__icontains=username)
        return queryset

    @extend_schema(
        responses={200: TicketListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={200: TicketDetailSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
