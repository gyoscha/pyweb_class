from django.contrib import admin

from . import models


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
