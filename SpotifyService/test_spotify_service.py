import pytest
from unittest.mock import Mock, patch
from SpotifyService.schemas import ConstructQueryInput
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
    "input_query, expected_query",
    [
        (
            {
                "track": "Bohemian Rhapsody",
                "artist": "Queen",
                "album": "A Night at the Opera",
            },
            "track:Bohemian Rhapsody artist:Queen album:A Night at the Opera",
        ),
        (
            {"track": "Imagine", "artist": "John Lennon"},
            "track:Imagine artist:John Lennon",
        ),
        (
            {"artist": "The Beatles", "album": "Abbey Road"},
            "artist:The Beatles album:Abbey Road",
        ),
        ({"track": "Yesterday"}, "track:Yesterday"),
        ({}, ""),
    ],
)
def test_construct_query(spotify_service, input_query, expected_query):
    input_query = ConstructQueryInput(**input_query)
    query = spotify_service._construct_query(input_query=input_query)
    assert query == expected_query


def test_construct_query_with_special_characters(spotify_service):
    input_query = ConstructQueryInput(track="Don't Stop Me Now", artist="Queen")
    query = spotify_service._construct_query(input_query)
    assert query == "track:Don't Stop Me Now artist:Queen"

def test_construct_query_case_sensitivity(spotify_service):
    input_query1 = ConstructQueryInput(track="Hello", artist="Adele")
    input_query2 = ConstructQueryInput(track="HELLO", artist="ADELE")
    query1 = spotify_service._construct_query(input_query1)
    query2 = spotify_service._construct_query(input_query2)
    assert query1 != query2

def test_construct_query_extra_spaces(spotify_service):
    input_query = ConstructQueryInput(track="  Shape of You  ", artist="  Ed Sheeran  ")
    query = spotify_service._construct_query(input_query)
    assert query == "track:  Shape of You   artist:  Ed Sheeran  "
