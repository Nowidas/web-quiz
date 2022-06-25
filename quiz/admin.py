# Register your models here.
from django.contrib import admin

from .models import Test, Question, Choice, Test_event, Test_user

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Test_event)
admin.site.register(Test_user)
