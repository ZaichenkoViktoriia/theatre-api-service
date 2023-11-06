
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play, Performance, TheatreHall, Genre, Actor
from theatre.serializers import (
    PlayListSerializer,
    PlayDetailSerializer,
)

PLAY_URL = reverse("theatre:play-list")
PLAY_SESSION_URL = reverse("theatre:performance-list")


def detail_url(play_id: int):
    return reverse("theatre:play-detail", args=[play_id])


def image_upload_url(play_id):
    return reverse("theatre:play-upload-image", args=[play_id])


def sample_play(**params):
    defaults = {
        "title": "Sample play",
        "description": "Sample description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Drama",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "George", "last_name": "Clooney"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(
        name="Blue", rows=20, seats_in_row=20
    )

    defaults = {
        "show_time": "2022-06-02 14:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


class UnauthenticatedTheatreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTheatreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@user.com",
            "test123",
        )
        self.client.force_authenticate(self.user)

    def test_list_plays(self):
        sample_play()
        sample_play()

        res = self.client.get(PLAY_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_plays_by_actors(self):
        # Create actors
        actor1 = sample_actor(first_name="Actor1", last_name="Actor1")
        actor2 = sample_actor(first_name="Actor2", last_name="Actor2")

        # Create plays without associating actors
        play1 = sample_play(title="play1")
        play2 = sample_play(title="play2")
        play3 = sample_play(title="test_play_without_actors")

        # Use .set() to associate actors with plays
        play1.actors.set([actor1])
        play2.actors.set([actor2])

        # Define the actor IDs for filtering
        actor_ids = f"{actor1.id},{actor2.id}"

        # Send the GET request to filter plays by actors
        res = self.client.get(PLAY_URL, {"actors": actor_ids})

        # Define serializers for plays
        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        # Check that the filtered plays are in the response
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

        # Check that play3 is not in the results
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_plays_by_genres(self):
        play1 = sample_play(title="play1")
        play2 = sample_play(title="play2")

        genre1 = sample_genre(name="Fantasy")
        genre2 = sample_genre(name="Horror")

        play1.genres.add(genre1)
        play2.genres.add(genre2)

        play3 = sample_play(title="without genres")

        res = self.client.get(
            PLAY_URL,
            {"genres": f"{genre1.id}, {genre2.id}"}
        )

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_play_by_title(self):
        play1 = sample_play(title="play1")
        play2 = sample_play(title="play2")

        res = self.client.get(PLAY_URL, {"title": "play1"})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_play_detail(self):
        play = sample_play()
        play.genres.add(Genre.objects.create(name="test"))
        play.actors.add(Actor.objects.create(
            first_name="Test", last_name="Test")
        )

        url = detail_url(play.id)
        res = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_forbidden(self):
        payload = {
            "title": "Test",
            "description": "Test info",
        }

        res = self.client.post(PLAY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTheatreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@admin.com", "admin123", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_play_forbidden(self) -> None:
        payload = {
            "title": "Test play",
            "description": "Test description",
        }
        res = self.client.post(PLAY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_play_not_allowed(self):
        play = sample_play()
        url = detail_url(play.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_play_not_allowed(self) -> None:
        play = sample_play()
        url = detail_url(play.id)
        res = self.client.put(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
