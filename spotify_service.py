import json
import logging
import os

import requests
import spotipy
import streamlit as st
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from streamlit.logger import get_logger

LOGGER = get_logger(__file__)
LOGGER.setLevel(logging.DEBUG)

load_dotenv()


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
ACCESS_TOKEN_URL = os.getenv("ACCESS_TOKEN_URL")


class SpotifyService:
    def __init__(self, client_id, client_secret):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret,
            )
        )

    def _construct_query(
        self, track: str = None, artist: str = None, album: str = None
    ):
        query_list = []

        if track:
            query_list.append(f"track:{track}")
        if artist:
            query_list.append(f"artist:{artist}")
        if album:
            query_list.append(f"album:{album}")

        query_string = " ".join(query_list)

        return query_string

    @st.cache_data
    def search(
        _self, track: str = None, artist: str = None, album: str = None, limit: int = 10
    ):

        query_string = _self._construct_query(track, artist, album)
        results = _self.sp.search(q=query_string, limit=limit)

        search_results = []

        for idx, track in enumerate(results["tracks"]["items"]):
            artist_names = [artist["name"] for artist in track["artists"]]
            track_info = dict(
                track_name=track["name"],
                artist=", ".join(artist_names),
                album_image=track["album"]["images"][0]["url"],
                id=track["id"],
            )

            search_results.append(track_info)

        return search_results

    def get_access(dc=None, key=None):
        """Starts session to get access token."""
        session = requests.Session()

        cookies = {"sp_dc": dc, "sp_key": key}
        LOGGER.debug(f"\n\n ==>> ACCESS_TOKEN_URL: {ACCESS_TOKEN_URL}")
        response = session.get(ACCESS_TOKEN_URL, cookies=cookies)
        response.raise_for_status()
        data = response.content.decode("utf-8")
        config = json.loads(data)

        access_token = config["accessToken"]
        expires_timestamp = config["accessTokenExpirationTimestampMs"]
        expiration_date = int(expires_timestamp) // 1000

        return access_token


if __name__ == "__main__":
    spotify = SpotifyService(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    track = "yellow"
    artist = "coldplay"

    search = spotify.search(track=track, artist=artist)
