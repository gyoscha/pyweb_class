from rest_framework import serializers

from blog.models import Note, Comment


class CommentSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, obj: Comment):
        return {
            'value': obj.rating,
            'display': obj.get_rating_display()
        }

    class Meta:
        model = Comment
        fields = "__all__"


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
        fields = 'id', 'title', 'message', 'public', 'author'
        read_only_fields = ('author', )


class PublicListNoteSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",  # указываем новое поле для отображения
        read_only=True  # поле для чтения
    )

    comments = CommentSerializer(many=True, read_only=True)  # one-to-many-relationships

    class Meta:
        model = Note
        fields = (
            'title', 'message', 'create_at', 'update_at', 'public',  # из модели
            'author', 'comments',  # из сериализатора
        )


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class NoteDetailSerializer(serializers.ModelSerializer):
    """ Одна статья блога """
    author = serializers.SlugRelatedField(
        slug_field="username",  # указываем новое поле для отображения
        read_only=True  # поле для чтения
    )
    comments = CommentSerializer(many=True, read_only=True)  # one-to-many-relationships

    class Meta:
        model = Note
        fields = (
            'title', 'message', 'create_at', 'update_at', 'public',  # из модели
            'author', 'comments',  # из сериализатора
        )
