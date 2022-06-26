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
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reminder_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.TextField()
    img_link = models.CharField(max_length=200, blank=True, null=True)
    q_type = models.CharField(max_length=50)

    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    if_correct = models.BooleanField()

    def __str__(self):
        return self.choice_text


class Test_user(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    taken = models.BooleanField()
    score = models.IntegerField()

    def __str__(self):
        return str(self.user + "|" + self.choice)
