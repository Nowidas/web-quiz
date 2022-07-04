from django.db import models
from django.conf import settings

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Test_event(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Test_user")
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reminder_date = models.DateTimeField(blank=True, null=True)
    # time_to_complete = models.TimeField() # for now depend only on start end time

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.TextField()
    img_link = models.CharField(max_length=200, blank=True, null=True)
    q_type = models.CharField(max_length=50)

    def __str__(self):
        return self.question


class Test_user(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_event = models.ForeignKey(Test_event, on_delete=models.CASCADE)

    taken = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    max_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.test_event) + " - " + str(self.user.username)

    class Meta:
        unique_together = ("user", "test_event")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    picks = models.ManyToManyField(
        Test_user, blank=True, null=True, through="ChoicePerUser"
    )
    choice_text = models.CharField(max_length=200)
    if_correct = models.BooleanField()

    def __str__(self):
        return self.choice_text


class ChoicePerUser(models.Model):
    pick = models.ForeignKey(Choice, on_delete=models.CASCADE)
    test_user = models.ForeignKey(Test_user, on_delete=models.CASCADE)

    ans_time = models.DateTimeField()

    def __str__(self):
        return str(self.test_user) + " - " + str(self.pick)

    class Meta:
        unique_together = ("pick", "test_user")
