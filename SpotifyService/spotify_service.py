import json
import logging
import os
from typing import List

import requests
import spotipy
import streamlit as st
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from streamlit.logger import get_logger

from SpotifyService.schemas import (
    ConstructQueryInput,
    ConvertedSpotifySearchResult,
    SpotifySearchResult,
)

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

    def _construct_query(self, input_query: ConstructQueryInput) -> str:
        query_list = []

        if input_query.track:
            query_list.append(f"track:{input_query.track}")
        if input_query.artist:
            query_list.append(f"artist:{input_query.artist}")
        if input_query.album:
            query_list.append(f"album:{input_query.album}")

        query_string = " ".join(query_list)

        return query_string

    def _convert_search_result(
        self, result: SpotifySearchResult
    ) -> List[ConvertedSpotifySearchResult]:
        return [
            ConvertedSpotifySearchResult.from_spotify_search_result(item)
            for item in result.tracks.items
        ]

    @st.cache_data
    def search(
        _self, track: str = None, artist: str = None, album: str = None, limit: int = 10
    ) -> List[ConvertedSpotifySearchResult]:
        query_input = ConstructQueryInput(track=track, artist=artist, album=album)
        query_string = _self._construct_query(query_input)

        raw_results = _self.sp.search(q=query_string, limit=limit)
        results = SpotifySearchResult.from_dict(raw_results)

        return _self._convert_search_result(results)

    def get_access(dc=None, key=None):
        """Starts session to get access token."""
        session = requests.Session()

        cookies = {"sp_dc": dc, "sp_key": key}
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
