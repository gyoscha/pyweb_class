# Generated by Django 4.0.4 on 2022-05-23 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='create_at',
        ),
        migrations.AlterField(
            model_name='comment',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.note'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(choices=[(0, 'Без оценки'), (1, 'Ужасно'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')], default=0, verbose_name='Оценка'),
        ),
    ]
