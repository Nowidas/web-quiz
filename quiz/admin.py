# Register your models here.
from django.contrib import admin
import nested_admin

from .models import Test, Question, Choice, Test_event, Test_user, ChoicePerUser

admin.site.register(Question)
admin.site.register(Test_user)
admin.site.register(Choice)
admin.site.register(ChoicePerUser)


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


class UsersionInline(admin.TabularInline):
    model = Test_user
    extra = 1


class Test_eventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["test", "name"]}),
        ("Dates", {"fields": ["start_date", "end_date", "reminder_date"]}),
    ]
    inlines = [UsersionInline]


admin.site.register(Test_event, Test_eventAdmin)
