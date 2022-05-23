from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Note(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Текст статьи')
    public = models.BooleanField(default=False, verbose_name='Опубликовать')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    class RatingChoice(models.IntegerChoices):
        WITHOUT_RATING = 0, _('Без оценки')
        TERRIBLE = 1, _('Ужасно')
        BADLY = 2, _('Плохо')
        FINE = 3, _('Нормально')
        GOOD = 4, _('Хорошо')
        EXCELLENT = 5, _('Отлично')

    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE
    )
    rating = models.CharField(
        max_length=1,
        choices=RatingChoice.choices,
        default=RatingChoice.WITHOUT_RATING,
        verbose_name='Оценка'
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

