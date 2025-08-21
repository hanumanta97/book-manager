from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book

class BookAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse('book-list')

    def test_create_and_retrieve_book(self):
        payload = {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "published_date": "1999-10-30",
            "is_available": True
        }
        res = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book_id = res.data['id']

        # retrieve
        detail_url = reverse('book-detail', args=[book_id])
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], payload['title'])

    def test_update_and_delete_book(self):
        book = Book.objects.create(title="Old", author="Anon")
        detail_url = reverse('book-detail', args=[book.id])

        update = {"title": "New Title", "author": "Anon", "is_available": False}
        res = self.client.put(detail_url, update, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], "New Title")

        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
