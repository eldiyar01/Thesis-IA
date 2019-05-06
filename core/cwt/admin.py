from django.contrib import admin

from .models import Question, Test, Variant, Answer


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestonAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

