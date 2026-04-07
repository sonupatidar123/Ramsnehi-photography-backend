from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import GalleryItem, Film


class GalleryAPITest(APITestCase):

    def setUp(self):
        self.gallery_url = reverse('gallery-list')  # router se name aata hai

        GalleryItem.objects.create(
            title="Test Image",
            image="gallery/test.jpg",
            category="Wedding"
        )

    def test_get_gallery(self):
        response = self.client.get(self.gallery_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)


class FilmAPITest(APITestCase):

    def setUp(self):
        self.film_url = reverse('film-list')

        self.film = Film.objects.create(
            title="Test Film",
            type="Cinematic Film",
            video_id="https://youtu.be/gsgNnamwTVk"
        )

    def test_get_films(self):
        response = self.client.get(self.film_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_id_cleaning(self):
        self.assertEqual(self.film.video_id, "gsgNnamwTVk")

    def test_thumbnail_generation(self):
        self.assertIn("img.youtube.com", self.film.thumbnail_url)


class FilmCreateAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('film-list')

    def test_create_film(self):
        data = {
            "title": "New Film",
            "type": "Cinematic Film",
            "video_id": "https://youtu.be/gsgNnamwTVk"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 1)