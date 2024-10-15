from django.urls import path

from user_config.views import (
    CreateUserView,
    LoginUserView,
    ManageUserView,
)

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("manage/", ManageUserView.as_view(), name="manage"),
]