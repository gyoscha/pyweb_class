from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404

from blog.models import Note
from . import serializers, filters


# выводим только опубликованные записи
class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()   # Переопределяем данные
    serializer_class = serializers.NoteSerializer   # Переопределяем сериалайзер

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(public=True)


class UserNoteListAPIView(APIView):
    def get(self, request: Request, pk) -> Response:
        user_data = get_object_or_404(User, pk=pk)

        data = Note.objects.all()

        data_filtered = filters.filter_notes_by_username(data, username=user_data)

        serializer = serializers.NoteSerializer(
            instance=data_filtered,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class NoteListCreateAPIView(APIView):
    def get(self, request: Request) -> Response:
        note = Note.objects.all()

        serializer = serializers.NoteSerializer(
            instance=note,
            many=True,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = serializers.NoteSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)   # Проверка на правильность введенных данных из request
        serializer.save(author=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class NoteDetailAPIView(APIView):
    def get(self, request: Request, pk) -> Response:
        note_data = get_object_or_404(Note, pk=pk)

        serializer = serializers.NoteSerializer(
            instance=note_data,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        note_data = get_object_or_404(Note, pk=pk)
        note_data.title = request.data['title']
        note_data.message = request.data['message']
        note_data.save()

        serializer = serializers.NoteSerializer(
            instance=note_data,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk) -> Response:
        note_data = get_object_or_404(Note, pk=pk)

        serializer = serializers.NoteSerializer(
            instance=note_data,
            data=request.data,
            partial=True   # для частичного обновления данных
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk) -> Response:
        note_data = get_object_or_404(Note, pk=pk)
        note_data.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
