from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from .views import (
    LogoutView,
    UserRegistrationView,
    CurrentUserView,
    MyCandidateProfileView,
    MyRecruiterProfileView
)

app_name = 'accounts'

urlpatterns = [
    path(
        'register/',
        UserRegistrationView.as_view(),
        name='user-registration'
        ),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),
    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="refresh",
    ),
    path(
        "me/",
        CurrentUserView.as_view(),
        name="me",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "candidate/me/",
        MyCandidateProfileView.as_view(),
        name="candidate-profile",
    ),
    path(
        "recruiter/me/",
        MyRecruiterProfileView.as_view(),
        name="recruiter-profile",
    ),
]