from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quizzes", views.quizzes, name="quizzes"),
    path("<int:quiz_id>/", views.quiz_details, name="quiz_details"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout, name="logout"),
]
