from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404

from blog.models import Note
from . import serializers


# выводим только опубликованные записи
class PublicNoteListAPIView(ListAPIView):
    queryset = Note.objects.all()   # Переопределяем данные
    serializer_class = serializers.NoteSerializer   # Переопределяем сериалайзер

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(public=True)


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

        # serial = serializers.BlogSerializer(note_data)

        # return Response(serial.data, status=status.HTTP_200_OK)
        return Response(serializers.note_serializer(note_data), status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        note_data = get_object_or_404(Note, pk=pk)
        note_data.title = request.data['title']
        note_data.message = request.data['message']
        note_data.save()

        # serial = serializers.BlogSerializer(note_data)
        #
        # return Response(serial.data, status=status.HTTP_200_OK)
        return Response(serializers.note_serializer(note_data), status=status.HTTP_200_OK)
