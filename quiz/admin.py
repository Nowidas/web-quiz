# Register your models here.
from django.contrib import admin
import nested_admin

from .models import Test, Question, Choice, Test_event, Test_user

admin.site.register(Question)
admin.site.register(Test_event)
admin.site.register(Test_user)


class ChoiceionInline(nested_admin.NestedStackedInline):
    model = Choice
    extra = 1


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceionInline]


class TestAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [(None, {"fields": ["name", "description"]})]
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)
