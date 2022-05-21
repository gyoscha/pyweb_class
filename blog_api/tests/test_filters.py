# Привязки к API тут нет
from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Note
from blog_api import filters


class TestNoteFilter(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user_1 = User(username='user_1', password='user_1')   # Они не попали еще в базу данных
        test_user_2 = User(username='user_2', password='user_2')

        test_user_1, test_user_2 = User.objects.bulk_create([test_user_1, test_user_2])   # теперь попали

        Note.objects.create(title='TEST_title', message='TEST_msg', author=test_user_1, public=True)
        Note.objects.create(title='TEST_title_2', message='TEST_msg_2', author=test_user_2, public=True)

    def test_filter_notes_by_author_id(self):
        filter_author_id = 1
        queryset = Note.objects.all()

        expected_queryset = queryset.filter(author_id=filter_author_id)
        actual_queryset = filters.filter_notes_by_author_id(queryset, filter_author_id)

        self.assertQuerysetEqual(expected_queryset, actual_queryset)

    def test_filter_notes_by_username(self):
        username = 'user_1'
        queryset = Note.objects.all()

        expected_queryset = queryset.filter(author__username=username)
        actual_queryset = filters.filter_notes_by_username(queryset, username)

        self.assertQuerysetEqual(expected_queryset, actual_queryset)