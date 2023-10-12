from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Create your views here.

# class BookListApiView(generics.ListAPIView):
#         queryset = Book.objects.all()
#         serializer_class = BookSerializer

class BookListApiView(APIView):
        def get(self, request):
                books = Book.objects.all()
                serializer_data = BookSerializer(books, many=True).data

                data = {
                        'status':f'Returned {len(books)} books',
                        'books':serializer_data
                }

                return Response(data)
        

class BookDetailApiView(APIView):
        def get(self, request, pk):
                try:
                        book = Book.objects.get(id=pk)
                        serializer_data = BookSerializer(book).data

                        data = {
                                'status':'Successful',
                                'book':serializer_data
                        }

                        return Response(data)
                except Exception:
                        return Response(
                                {
                                        'status':'Does not exist',
                                        'message':'Book not found'
                                },
                                status=status.HTTP_404_NOT_FOUND
                        )
                

# class BookDeleteApiView(generics.DestroyAPIView):
#         queryset = Book.objects.all()
#         serialzer_class = BookSerializer

class BookDeleteApiView(APIView):
        def delete(self, request, pk):
                try:
                        book = Book.objects.get(id=pk)
                        book.delete()

                        return Response({
                                'status':True,
                                'message':'Succesfully deleted'
                        })
                except Exception:
                        return Response({
                                'status':False,
                                'message':'Book is not found' 
                        })


# class BookUpdateApiView(generics.UpdateAPIView):
#         queryset = Book.objects.all()
#         serializer_class = BookSerializer

class BookUpdateApiView(APIView):
        def put(self, request, pk):
                book = get_object_or_404(Book, id=pk)
                data = request.data
                serialized_data = BookSerializer(instance=book, data=data, partial=True)

                if serialized_data.is_valid(raise_exception=True):
                        book_saved = serialized_data.save()
                        return Response({
                                'status':True,
                                'message':'The book is updated'
                        })

# class BookCreateApiView(generics.CreateAPIView):
#         queryset = Book.objects.all()
#         serializer_class = BookSerializer

class BookCreateApiView(APIView):
        def post(self, request):
                data = request.data 
                serializer = BookSerializer(data=data)

                if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        data = {
                                'status':'Book created!',
                                'data':data
                        }
                        return Response(data)
                else:
                        return Response(
                                {
                                        'status':False,
                                        'message':'Seriazlizer is not valid'
                                },
                                status.HTTP_400_BAD_REQUEST
                        )

# class BookListCreateApiView(generics.ListCreateAPIView):
#         queryset = Book.objects.all()
#         serializer_class = BookSerializer

class BookUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
        queryset = Book.objects.all()
        serializer_class = BookSerializer


class BookViewSet(ModelViewSet):
        queryset = Book.objects.all()
        serializer_class = BookSerializer

@api_view(['GET'])
def book_list_view(request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)
