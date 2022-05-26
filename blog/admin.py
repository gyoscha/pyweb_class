from django.contrib import admin

from . import models


# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#inlinemodeladmin-objects
class CommentInline(admin.TabularInline):
    model = models.Comment

    extra = 0
    min_num = 0


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    # отображение связи Many-to-one
    inlines = [
        CommentInline
    ]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
