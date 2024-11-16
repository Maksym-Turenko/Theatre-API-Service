from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_config.views import (
    CreateUserView,
    ManageUserView,
)

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("manage/", ManageUserView.as_view(), name="manage"),
]
