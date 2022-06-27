from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages

from .models import Test

# Create your views here.
@login_required
def index(request):
    return render(request, "quiz/index.html")


@login_required
def quizzes(request):
    quizzes = Test.objects.all()
    return render(request, "quiz/quizzes.html", {"quizzes": quizzes})


@login_required
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
            return redirect("/quizzes")
        else:
            messages.error(request, "Bad credencials")
            return render(request, "quiz/login.html")
    else:
        return render(request, "quiz/login.html")


def signup_page(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
            messages.error(request, "Email taken")
            return render(request, "quiz/signup.html")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            messages.success(request, "Account created.")
            return redirect("/quizzes")
    else:
        return render(request, "quiz/signup.html")


@login_required
def logout_page(request):
    logout(request)
    return redirect("/quizzes")
