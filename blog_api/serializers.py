from rest_framework import serializers

from blog.models import Note


# Делал на практике сам 12.05.
def note_serializer(note) -> dict:
    return {
        'id': note.id,
        'title': note.title,
        'message': note.message,
        'public': note.public,
    }


# Делал на практике сам 12.05.
class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField
    title = serializers.CharField(max_length=300)
    message = serializers.CharField(max_length=300)
    public = serializers.BooleanField
    create_at = serializers.DateTimeField
    update_at = serializers.DateTimeField


# Практика от 19.05.
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('author', )
