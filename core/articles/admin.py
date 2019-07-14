from django.contrib import admin

from .models import Article, Category


@admin.register(Article)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class TestAdmin(admin.ModelAdmin):
    pass    