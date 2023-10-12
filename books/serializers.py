from .models import Book
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'subtitle', 'isbn', 'price', 'author', 'content')

    def validate(self, data):
        title = data.get('title', None)
        author = data.get('author', None)

        # Check the title is contains only letters
        if not title.isalpha():
            raise ValidationError(
                {
                    'status':False,
                    'message':'Only letters are allowed'
                }
            )
        
        # check the book exists in database
        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError(
                {

                    'status':False,
                    'message':'Book is already exists in database!'
                }
            )
        return data