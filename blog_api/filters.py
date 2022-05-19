def filter_notes_by_author_id(queryset, author_id):
    """
    Фильтруем записи по author_id
    :param queryset: записи
    :param author_id: id автора
    :return: Список записей этого автора
    """
    return queryset.filter(author_id=author_id)
