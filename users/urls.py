from django.contrib.auth.views import LogoutView
from django.urls import path

from users import apps
from users.views import CustomLoginView, RegisterView, UserUpdateView

app_name = apps.UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
]
