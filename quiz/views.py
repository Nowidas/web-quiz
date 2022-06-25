from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "quiz/index.html")


def quizzes(request):
    return render(request, "quiz/quizzes.html")


def login(request):
    return render(request, "quiz/login.html")


def signup(request):
    return render(request, "quiz/signup.html")


def logout(request):
    return render(request, "quiz/index.html")
