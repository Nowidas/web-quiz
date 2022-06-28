import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages

from .models import Choice, ChoicePerUser, Question, Test, Test_event, Test_user

# Create your views here.
@login_required
def index(request):
    return render(request, "quiz/index.html")


@login_required
def quizzes(request):
    infooo = Test_user.objects.all().filter(user=request.user.id).order_by("start_date")
    return render(request, "quiz/quizzes.html", {"quiz_event": infooo})


@login_required
def quiz_details(request, quiz_id):
    try:
        quiz = get_object_or_404(Test_user, user=request.user.id, test_event=quiz_id)
    except Test.DoesNotExist:
        raise Http404("Quiz does not exist")
    return render(request, "quiz/detail.html", {"quiz": quiz})


@login_required
def quiz_logic(request, quiz_id, question_nb):
    try:
        quiz = get_object_or_404(Test_user, user=request.user.id, test_event=quiz_id)
        questions = Question.objects.all().filter(test=quiz.test_event.test.id)
        choices = Choice.objects.all().filter(question=questions[question_nb].id)
        user_picks = (
            ChoicePerUser.objects.all()
            .filter(test_user=quiz.id, pick__in=choices)
            .values_list("pick", flat=True)
        )
    except Test.DoesNotExist:
        raise Http404("Quiz does not exist")

    if request.method == "POST":
        print("POST")
        # print(request.POST)
        if "ans" in request.POST:
            # print(request.POST.getlist("ans"))
            ChoicePerUser.objects.all().filter(
                test_user=quiz.id, pick__in=choices
            ).delete()
            #### Choice.objects.all().filter(question=quiz.test_event.test.id)
            picked = choices.filter(pk__in=request.POST.getlist("ans"))
            print(picked)
            for i in range(len(picked)):
                picked[i].picks.add(
                    quiz.id,
                    through_defaults={"ans_time": datetime.date.today()},
                )

        if "DONE" in request.POST:
            return redirect("summary", quiz_id=quiz_id)
        else:
            return redirect(
                "quiz_logic", quiz_id=quiz_id, question_nb=request.POST["click"]
            )
    else:
        return render(
            request,
            "quiz/question.html",
            {
                "quiz": quiz,
                "question": questions[question_nb],
                "choices": choices,
                "question_nb": question_nb,
                "quiz_len": len(questions),
                "range": range(len(questions)),
                "user_picks": list(user_picks),
            },
        )


@login_required
def summary(request, quiz_id):
    return render(request, "quiz/index.html")


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
