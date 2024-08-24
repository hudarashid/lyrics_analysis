import pytest
from unittest.mock import Mock, patch
from SpotifyService.spotify_service import (
    SpotifyService,
)


@pytest.fixture
def spotify_service():
    return SpotifyService("dummy_client_id", "dummy_client_secret")


@patch("SpotifyService.spotify_service.spotipy.Spotify")
@patch("SpotifyService.spotify_service.SpotifyClientCredentials")
def test_spotify_service_initialization(mock_credentials, mock_spotify):
    client_id = "test_client_id"
    client_secret = "test_client_secret"

    SpotifyService(client_id, client_secret)

    mock_credentials.assert_called_once_with(
        client_id=client_id, client_secret=client_secret
    )
    mock_spotify.assert_called_once_with(auth_manager=mock_credentials.return_value)


@pytest.mark.parametrize(
    "track, artist, album, expected_query",
    [
        (
            "Bohemian Rhapsody",
            "Queen",
            "A Night at the Opera",
            "track:Bohemian Rhapsody artist:Queen album:A Night at the Opera",
        ),
        ("Imagine", "John Lennon", None, "track:Imagine artist:John Lennon"),
        (None, "The Beatles", "Abbey Road", "artist:The Beatles album:Abbey Road"),
        ("Yesterday", None, None, "track:Yesterday"),
        (None, None, None, ""),
    ],
)
def test_construct_query(spotify_service, track, artist, album, expected_query):
    query = spotify_service._construct_query(track=track, artist=artist, album=album)
    assert query == expected_query


def test_construct_query_with_special_characters(spotify_service):
    query = spotify_service._construct_query(track="Don't Stop Me Now", artist="Queen")
    assert query == "track:Don't Stop Me Now artist:Queen"


def test_construct_query_case_sensitivity(spotify_service):
    query1 = spotify_service._construct_query(track="Hello", artist="Adele")
    query2 = spotify_service._construct_query(track="HELLO", artist="ADELE")
    assert query1 == query2


def test_construct_query_extra_spaces(spotify_service):
    query = spotify_service._construct_query(
        track="  Shape of You  ", artist="  Ed Sheeran  "
    )
    assert query == "track:Shape of You artist:Ed Sheeran"
