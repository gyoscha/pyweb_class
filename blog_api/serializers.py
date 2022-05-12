from abc import ABC

from rest_framework import serializers


def note_serializer(note) -> dict:
    return {
        'id': note.id,
        'title': note.title,
        'message': note.message,
        'public': note.public,
        'create_at': note.create_at,
        'update_at': note.update_at,
    }


class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField
    title = serializers.CharField(max_length=300)
    message = serializers.CharField(max_length=300)
    public = serializers.BooleanField
    create_at = serializers.DateTimeField
    update_at = serializers.DateTimeField
