from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("results", views.search_results, name="search_results")

]