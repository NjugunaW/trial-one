from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(QuizApp)
admin.site.register(QuizCategory)

class AnswerAdmin(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)