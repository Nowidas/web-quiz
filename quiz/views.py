from datetime import datetime, timezone
from pdb import line_prefix
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages

from django.db.models import OuterRef, Subquery
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
    if_start = (
        quiz.test_event.start_date < datetime.now(timezone.utc)
        and quiz.test_event.end_date > datetime.now(timezone.utc)
        and not quiz.taken
    )
    if_taken = quiz.taken
    return render(
        request,
        "quiz/detail.html",
        {"quiz": quiz, "start": if_start, "taken": if_taken},
    )


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
    print(user_picks)
    if quiz.test_event.start_date < datetime.now(timezone.utc):
        if request.method == "POST":
            print("POST")
            if (
                quiz.test_event.end_date >= datetime.now(timezone.utc) or not user_picks
            ) and not quiz.taken:
                ChoicePerUser.objects.all().filter(
                    test_user=quiz.id, pick__in=choices
                ).delete()
                if "ans" in request.POST:
                    picked = choices.filter(pk__in=request.POST.getlist("ans"))
                    print(datetime.today())
                    for i in range(len(picked)):
                        picked[i].picks.add(
                            quiz.id,
                            through_defaults={"ans_time": datetime.today()},
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
    else:
        return redirect("quiz_details", quiz_id=quiz_id)


@login_required
def summary(request, quiz_id):
    quiz = get_object_or_404(Test_user, user=request.user.id, test_event=quiz_id)
    questions = Question.objects.all().filter(test=quiz.test_event.test.id)
    all_choices = Choice.objects.all().filter(question_id__in=questions.values("id"))
    all_user_pick = ChoicePerUser.objects.all().filter(
        pick__in=all_choices.values("id"), test_user=quiz.id
    )

    first_date = Subquery(
        ChoicePerUser.objects.all()
        .filter(
            test_user=quiz.id,
            pick__question=OuterRef("question_id"),
        )
        .values("ans_time")[:1]
    )
    all_choices = all_choices.annotate(ans_time=first_date)

    # if test end calculate score
    # if not quiz.taken:
    if True:
        quiz.taken = True
        quiz.score = 0
        for i in range(len(questions)):
            choices = all_choices.filter(question_id=questions[i].id)
            user_picks = all_user_pick.all().filter(
                test_user=quiz.id, pick__in=choices.values("id")
            )
            right_choices = choices.filter(if_correct=True)
            if (
                set(right_choices.values_list("id", flat=True))
                == set(user_picks.values_list("pick", flat=True))
                and user_picks.first().ans_time <= quiz.test_event.end_date
            ):
                quiz.score += 1
        quiz.save()
    return render(
        request,
        "quiz/summary.html",
        {
            "quiz": quiz,
            "questions": questions,
            "all_choices": all_choices,
            "all_user_pick": set(all_user_pick.values_list("pick", flat=True)),
            "test_event": quiz.test_event,
        },
    )


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
