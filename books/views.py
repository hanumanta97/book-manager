from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-published_date', 'id')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    # bonus: filtering, search, ordering set in REST_FRAMEWORK
    filterset_fields = ['author', 'is_available']
    search_fields = ['title', 'author', 'is_available']
    ordering_fields = ['published_date', 'title', 'author', 'id']
