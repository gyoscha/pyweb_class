from abc import ABC

from rest_framework import serializers


def note_serializer(note) -> dict:
    return {
        'id': note.id,
        'title': note.title,
        'message': note.message,
        'public': note.public,
    }


class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField
    title = serializers.CharField(max_length=300)
    message = serializers.CharField(max_length=300)
    public = serializers.BooleanField
    create_at = serializers.DateTimeField
    update_at = serializers.DateTimeField
