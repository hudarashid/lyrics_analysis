from typing import Dict, List, Optional
from pydantic import BaseModel


class ConstructQueryInput(BaseModel):
    track: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None


class SpotifyAlbumImages(BaseModel):
    height: int
    width: int
    url: str


class SpotifyArtists(BaseModel):
    external_urls: Dict[str, str]
    href: str
    id: str
    name: str
    type: str
    uri: str


class SpotifyAlbum(BaseModel):
    album_type: str
    artists: List[SpotifyArtists]
    available_markets: List[str]
    external_urls: Dict[str, str]
    href: str
    id: str
    images: List[SpotifyAlbumImages]
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str


class SpotifySearchResultItems(BaseModel):
    album: SpotifyAlbum
    artists: List[SpotifyArtists]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: Dict[str, str]
    external_urls: Dict[str, str]
    href: str
    id: str
    is_local: bool
    name: str
    popularity: int
    preview_url: Optional[str] = None
    track_number: int
    type: str
    uri: str


class SpotifySearchResultResponse(BaseModel):
    href: str
    items: List[SpotifySearchResultItems] = None
    limit: int
    next: Optional[str] = None
    offset: int
    previous: Optional[str] = None
    total: int


class SpotifySearchResult(BaseModel):
    tracks: SpotifySearchResultResponse

    @classmethod
    def from_dict(cls, data: Dict) -> "SpotifySearchResult":
        return cls(tracks=SpotifySearchResultResponse(**data["tracks"]))


class ConvertedSpotifySearchResult(BaseModel):
    track_name: str
    artist: str
    album_image: str
    id: str

    @classmethod
    def from_spotify_search_result(
        cls, item: SpotifySearchResultItems
    ) -> "ConvertedSpotifySearchResult":
        artist_names = [artist.name for artist in item.artists]
        return cls(
            track_name=item.name,
            artist=", ".join(artist_names),
            album_image=item.album.images[0].url if item.album.images else "",
            id=item.id,
        )
