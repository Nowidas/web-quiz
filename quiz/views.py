from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib import messages

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


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/quizzes.html")
        else:
            messages.error(request, "Bad credencials")
            return render(request, "quiz/login.html")
    else:
        return render(request, "quiz/login.html")


def signup(request):
    return render(request, "quiz/signup.html")


def logout(request):
    return render(request, "quiz/index.html")
