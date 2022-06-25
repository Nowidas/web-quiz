from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Test

# Create your views here.
def index(request):
    return render(request, "quiz/index.html")


def quizzes(request):
    quizzes = Test.objects.all()
    return render(request, "quiz/quizzes.html", {"quizzes": quizzes})


def quiz_details(request, quiz_id):
    try:
        quiz = get_object_or_404(Test, pk=quiz_id)
    except Test.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "quiz/detail.html", {"quiz": quiz})


def login(request):
    return render(request, "quiz/login.html")


def signup(request):
    return render(request, "quiz/signup.html")


def logout(request):
    return render(request, "quiz/index.html")
