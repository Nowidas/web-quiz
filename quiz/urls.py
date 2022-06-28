from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quizzes", views.quizzes, name="quizzes"),
    path("quiz/<int:quiz_id>/", views.quiz_details, name="quiz_details"),
    path("quiz/<int:quiz_id>/<int:question_nb>/", views.quiz_logic, name="quiz_logic"),
    path("quiz/<int:quiz_id>/summary", views.summary, name="summary"),
    path("login", views.login_page, name="login"),
    path("signup", views.signup_page, name="signup"),
    path("logout", views.logout_page, name="logout"),
]
