from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Текст статьи')
    public = models.BooleanField(default=False, verbose_name='Опубликовать')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
