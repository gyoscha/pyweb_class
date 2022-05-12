from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from blog.models import Note
from . import serializers


class NoteListCreateAPIView(APIView):
    def get(self, request: Request) -> Response:
        note = Note.objects.all()
        return Response(
            [serializers.note_serializer(word) for word in note],
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        req = request.data
        req_note = Note(**req)
        req_note.save(force_insert=True)

        # return Response(
        #     serializers.note_serializer(req),
        #     status=status.HTTP_201_CREATED
        # )
        serial = serializers.BlogSerializer(req)

        return Response(
            serial.data,
            status=status.HTTP_201_CREATED
        )


class NoteDetailAPIView(APIView):
    def get(self, request: Request, pk) -> Response:
        note_data = get_object_or_404(Note, pk=pk)

        serial = serializers.BlogSerializer(note_data)

        return Response(serial.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        note_data = get_object_or_404(Note, pk=pk)
        note_data.title = request.data['title']
        note_data.message = request.data['message']
        note_data.save()

        serial = serializers.BlogSerializer(note_data)

        return Response(serial.data, status=status.HTTP_200_OK)
