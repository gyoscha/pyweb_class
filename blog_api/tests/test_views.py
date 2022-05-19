from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from blog.models import Note


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

    def test_create_objects(self):
        url = '/notes/'

        new_title = 'test_title'
        new_message = 'test_message'
        data = {
            'title': new_title,
            'message': new_message,
        }

        resp = self.client.post(url, data=data)

        expected_status_code = status.HTTP_201_CREATED
        self.assertEqual(expected_status_code, resp.status_code)

        self.assertTrue(Note.objects.get(pk=1))
        self.assertFalse(Note.objects.get(pk=2))


class TestNoteDetailAPIView(APITestCase):
    """
    TESTS:
    1. Получение существующей записи в блоге;
    2. Получение несуществующей записи в блоге;
    3. Обновление существующей записи в блоге;
    4. Обновление несуществующей записи в блоге.

    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test@test.ru', password='123456')
        Note.objects.create(title='TEST_title', message='TEST_msg', author_id=1)

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
