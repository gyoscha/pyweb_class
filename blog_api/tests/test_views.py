from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

from blog.models import Note, Comment


class TestPublicNoteListAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка
    2. Получение отфильтрованного списка записей (только public)
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test@test.ru', password='123456')

    def test_empty_list_objects(self):
        url = '/notes/public/'

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение пустого списка записей
        response_data = resp.data
        expected_data = []
        self.assertEqual(expected_data, response_data)

    def test_public_list_objects(self):
        url = '/notes/public/'

        Note.objects.create(title='TEST_title', message='TEST_msg', author_id=1, public=True)
        Note.objects.create(title='TEST_title_2', message='TEST_msg_2', author_id=1, public=True)
        Note.objects.create(title='TEST_title_3', message='TEST_msg_3', author_id=1, public=False)

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение списка записей
        response_data = resp.data
        expected_data = 2
        self.assertEqual(expected_data, len(response_data))

        for note in response_data:
            self.assertTrue(note['public'])


class TestNoteListCreateAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка записей в блоге;
    2. Получение списка  записей в блоге;
    3. Создание записи в блоге.
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test@test.ru', password='123456')

        User.objects.create_user(username='test_1', password='1234567')

    def test_empty_list_objects(self):
        url = '/notes/'
        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение пустого списка
        response_data = resp.data
        expected_data = []
        self.assertEqual(expected_data, response_data)

    def test_list_objects(self):
        url = '/notes/'

        Note.objects.create(title='Test title', message='Test_msg', author_id=1)

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение списка записей
        response_data = resp.data
        expected_data = 1
        self.assertEqual(expected_data, len(response_data))

    def test_login(self):
        resp = self.client.login(username='test_1', password='1234567')

        self.assertTrue(resp)

    def test_create_objects(self):
        url = '/notes/'

        new_title = 'test_title'
        new_message = 'test_message'
        data = {
            'title': new_title,
            'message': new_message,
        }

        self.client.login(username='test_1', password='1234567')

        resp = self.client.post(url, data=data)

        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(expected_status_code, resp.status_code)

        self.assertTrue(Note.objects.get(pk=1))


class TestNoteDetailAPIView(APITestCase):
    """
    TESTS:
    1. Получение существующей записи в блоге;
    2. Получение несуществующей записи в блоге;
    3. Обновление существующей записи в блоге;
    4. Обновление несуществующей записи в блоге.
    5. Частичное обновление записи
    6. Удаление записи

    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test@test.ru', password='123456')
        Note.objects.create(title='TEST_title', message='TEST_msg', author_id=1)
        Note.objects.create(title='TEST_title_2', message='TEST_msg_2', author_id=1)

    def test_retrieve_existing_object(self):
        pk = 1
        url = f'/notes/{pk}'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            'id': 1,
            'title': 'TEST_title',
            'message': 'TEST_msg',
            'public': False,
            'author': 1,
            "comments": []
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_retrieve_non_existent_object(self):
        pk = 11
        url = f'/notes/{pk}'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_update_existing_object(self):
        pk = 1
        url = f'/notes/{pk}'

        put_data = {
            'title': 'TEST_title_PUT',
            'message': 'TEST_msg_PUT',
        }
        resp = self.client.put(url, put_data)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            'id': 1,
            'title': 'TEST_title_PUT',
            'message': 'TEST_msg_PUT',
            'public': False,
            'author': 1,
            "comments": []
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_update_non_existent_object(self):
        pk = 11
        url = f'/notes/{pk}'

        put_data = {
            'title': 'TEST_title_PUT',
            'message': 'TEST_msg_PUT',
        }
        resp = self.client.put(url, put_data)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)

    def test_patch_title(self):
        pk = 2
        url = f'/notes/{pk}'

        patch_data_1 = {
            'title': 'TEST_title_patch',
        }

        resp = self.client.patch(url, patch_data_1)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            'id': 2,
            'title': 'TEST_title_patch',
            'message': 'TEST_msg_2',
            'public': False,
            'author': 1,
            "comments": []
        }
        self.assertDictEqual(expected_data, resp.data)

    def test_patch_message(self):
        pk = 1
        url = f'/notes/{pk}'

        patch_data_2 = {
            'message': 'TEST_msg_patch',
        }

        resp = self.client.patch(url, patch_data_2)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            'id': 1,
            'title': 'TEST_title',
            'message': 'TEST_msg_patch',
            'public': False,
            'author': 1,
            "comments": []
        }
        self.assertDictEqual(expected_data, resp.data)

    def test_delete(self):
        pk = 1
        url = f'/notes/{pk}'

        resp = self.client.delete(url)

        expected_status_code = status.HTTP_204_NO_CONTENT
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = None

        self.assertEqual(expected_data, resp.data)


class TestUserNoteListAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка записей по данному автору;
    2. Получение списка записей по данному автору;
    3. Отсутствие заданного автора.
    """

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test_1', password='1234567')
        User.objects.create(username='test_2', password='1234567')
        User.objects.create(username='test_3', password='1234567')

        Note.objects.create(title='TEST_title_1', message='TEST_msg_1', author_id=1)
        Note.objects.create(title='TEST_title_2', message='TEST_msg_2', author_id=2)
        Note.objects.create(title='TEST_title_3', message='TEST_msg_3', author_id=1)
        Note.objects.create(title='TEST_title_4', message='TEST_msg_4', author_id=1)

    def test_empty_list(self):
        pk = 3
        url = f'/users/{pk}/notes/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = []

        self.assertEqual(expected_data, resp.data)

    def test_list_objects(self):
        pk = 2
        url = f'/users/{pk}/notes/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = [{
            'id': 2,
            'title': 'TEST_title_2',
            'message': 'TEST_msg_2',
            'public': False,
            'author': 2,
        }]

        self.assertEqual(expected_data, resp.data)

    def test_non_existent_author(self):
        pk = 4
        url = f'/users/{pk}/notes/'

        resp = self.client.get(url)

        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(expected_status_code, resp.status_code)

        expected_data = {
            "detail": "Not found."
        }

        self.assertDictEqual(expected_data, resp.data)


class TestCommentNoteListCreateAPIView(APITestCase):
    """
    TESTS:
    1. Получение пустого списка комментраев;
    2. Получение списка  комментариев;
    3. Создание комментария.
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test_1', password='1234567')

        User.objects.create_user(username='test_2', password='1234567')

    def test_empty_list_objects(self):
        url = '/notes/comments/'
        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение пустого списка
        response_data = resp.data
        expected_data = []
        self.assertEqual(expected_data, response_data)

    def test_list_objects(self):
        url = '/notes/comments/'

        Note.objects.create(title='TEST_title', message='TEST_msg', author_id=1)
        Note.objects.create(title='TEST_title_2', message='TEST_msg_2', author_id=1)

        Comment.objects.create(note_id=1, rating=3, author_id=1)

        resp = self.client.get(url)

        # Проверка статус кода
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(expected_status_code, resp.status_code)

        # Проверка на получение списка записей
        response_data = resp.data
        expected_data = 1
        self.assertEqual(expected_data, len(response_data))

    def test_create_objects(self):
        url = '/notes/comments/'

        Note.objects.create(title='TEST_title', message='TEST_msg', author_id=1)
        Note.objects.create(title='TEST_title_2', message='TEST_msg_2', author_id=1)

        data = {
             "rating": 1,
             "author": 1,
             "note": 2
        }

        resp = self.client.post(url, data=data)

        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(expected_status_code, resp.status_code)

        self.assertTrue(Note.objects.get(pk=1))
