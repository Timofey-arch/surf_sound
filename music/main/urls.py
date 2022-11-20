from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # path("register/", views.RegisterUser.as_view(), name="register")
    # path("", include("django.contrib.auth.urls"))
    path("signup/", views.signup, name="signup"),
]
