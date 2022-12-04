from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_auth, name="login_auth"),
    path("logout/", views.logout_auth, name="logout_auth"),
]
