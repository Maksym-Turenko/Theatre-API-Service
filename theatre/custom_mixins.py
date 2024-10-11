class UserInfoMixin:
    def get_user_username(self, obj):
        user = getattr(obj, "user", None) or getattr(obj.reservation, "user", None)
        return user.username if user else "No user"

    def get_user_email(self, obj):
        user = getattr(obj, "user", None) or getattr(obj.reservation, "user", None)
        return user.email if user else "No email"

    get_user_username.short_description = "Username"
    get_user_email.short_description = "Email"


class PlayInfoMixin:
    def get_play_title(self, obj):
        play = getattr(obj, "performance", None)
        return (
            play.play.title
            if play
            else obj.play.title if hasattr(obj, "play") else "No play"
        )

    get_play_title.short_description = "Play Title"


class TheatreHallInfoMixin:
    def get_theatre_hall_name(self, obj):
        return obj.theatre_hall.name if obj.theatre_hall else "No theatre hall"

    get_theatre_hall_name.short_description = "Theatre Hall Name"
