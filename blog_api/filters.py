from typing import Optional


def filter_notes_by_author_id(queryset, author_id):
    """
    Фильтруем записи по author_id
    :param queryset: записи
    :param author_id: id автора
    :return: Список записей этого автора
    """
    return queryset.filter(author_id=author_id)


def filter_notes_by_username(queryset, username):
    """
    Фильтруем записи по username
    :param queryset: записи
    :param username: автор
    :return: Список записей этого автора
    """
    return queryset.filter(author__username=username)


def note_create_at__year_filter(queryset, year: Optional[int]):
    """
    Фильтрация записей за указанный год.

    https://docs.djangoproject.com/en/4.0/ref/models/querysets/#year
    """
    if year is not None:
        return queryset.filter(create_at__year=year)
    else:
        return queryset


def note_update_at__month__gte_filter(queryset, month: Optional[int]):
    """
    Фильтрация записей за последние месяцы (больше или равные чем указанный месяц).

    https://docs.djangoproject.com/en/4.0/ref/models/querysets/#month
    """
    if month is not None:
        return queryset.filter(create_at__month__gte=month)
    else:
        return queryset


