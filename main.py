import logging
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_card import card

from lyrics_service import LyricsService
from spotify_service import SpotifyService

from streamlit.logger import get_logger

LOGGER = get_logger(__file__)
LOGGER.setLevel(logging.DEBUG)

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


spotify = SpotifyService(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
lyric_service = LyricsService()

st.title(f"Song Lyrics Analysis")
st.write(f"Search for any song title, artist name, or album.")
st.write(
    f"If the song lyrics are available, an analysis will be provided including word count, the top 10 most repeated words, unique words that appear only once, and phrases that are repeated multiple times."
)


search_form = st.form("search_form", clear_on_submit=True)
container = st.container(border=True)
col1, col2 = st.columns(2)

track_input = search_form.text_input(
    label="Track title", placeholder="Enter track title here..."
)
artists_input = search_form.text_input(
    label="Artist(s) name", placeholder="Enter artist(s) name here..."
)
album_input = search_form.text_input(
    label="Album name", placeholder="Enter album name here..."
)

submitted = search_form.form_submit_button("Search")

if submitted:
    if not track_input and not artists_input and not album_input:
        search_form.error(
            f"Please enter one of the following field: track/artist(s)/album."
        )

    else:
        search_results = spotify.search(
            track=track_input, artist=artists_input, album=album_input
        )

        if not search_results:
            if track_input:
                st.warning(
                    f"No search results found for Track title: _**{track_input}**_."
                )

            if artists_input:
                st.warning(
                    f"No search results found for Artist: _**{artists_input}**_."
                )

            if album_input:
                st.warning(f"No search results found for Album: _**{album_input}**_.")

        # Initialize session state for each track
        for index, result in enumerate(search_results):
            track_id = result["id"]
            track_name = result["track_name"]
            album_image = result["album_image"]
            artist = result["artist"]
            if track_id not in st.session_state:
                st.session_state[track_id] = track_name
                st.session_state[f"{track_id}_track_name"] = track_name
                st.session_state[f"{track_id}_album_image"] = album_image
                st.session_state[f"{track_id}_artist"] = artist

            # display results equally
            if index % 2 == 0:
                with col1:
                    card_result = card(
                        title=result["track_name"],
                        text=f"Song by {result['artist']}",
                        image=result["album_image"],
                        key=result["id"],
                    )
            else:
                with col2:
                    card_result = card(
                        title=result["track_name"],
                        text=f"Song by {result['artist']}",
                        image=result["album_image"],
                        key=result["id"],
                    )


# omit form, and Check if "FormSubmitter:search_form-Search" is False
if not st.session_state.get("FormSubmitter:search_form-Search"):
    # Find the key with a value of True (for card is clicked)
    for key, value in st.session_state.items():

        if value is True and key != "FormSubmitter:search_form-Search":
            result = lyric_service.get_lyrics(key)

            if not result:
                st.error(
                    f"No lyrics found for track _**{st.session_state.get(f'{key}_track_name')}**_."
                )
            else:
                combined_lyrics = lyric_service.combined_lyrics(result)

                _, sorted_repeated_phrases = lyric_service.find_repeated_phrases(
                    combined_lyrics
                )

                (
                    word_count,
                    most_common,
                    char_counts,
                    unique_words,
                    unique_words_count,
                ) = lyric_service.count_most_common("\n".join(combined_lyrics.values()))

                card(
                    title=f"{st.session_state.get(f'{key}_track_name')}",
                    text="Song by " + f"{st.session_state.get(f'{key}_artist')}",
                    image=f"{st.session_state.get(f'{key}_album_image')}",
                    styles={"card": {"pointer-events": "none"}},
                )

                if char_counts:
                    st.subheader(f"Word Counts: {word_count}", divider="rainbow")
                    for language, char_count in char_counts.items():
                        st.subheader(
                            f"{language} Character Counts: {char_count}",
                            divider="rainbow",
                        )

                else:
                    st.subheader(f"Word Counts: {word_count}", divider="rainbow")

                st.subheader(
                    f"Word Cloud for top 10 most repeated words:", divider="rainbow"
                )
                word_cloud_fig = lyric_service.create_word_cloud(most_common)
                st.pyplot(word_cloud_fig)

                df = pd.DataFrame(most_common, columns=["Word", "Count"])
                df.index = range(1, len(df) + 1)
                st.dataframe(df.style.hide(axis="index"))

                st.subheader(f"Word Cloud for Unique words", divider="rainbow")
                st.write(f"These are the words that appear only once in the track.")
                st.write(f"Unique words count: {unique_words_count} words")
                unique_word_cloud_fig = lyric_service.create_word_cloud(
                    {word: 1 for word in unique_words}
                )
                st.pyplot(unique_word_cloud_fig)

                st.subheader(f"Most repeated phrases:", divider="rainbow")
                df = pd.DataFrame(
                    sorted_repeated_phrases, columns=["Phrase", "Repeated times"]
                )
                df.index = range(1, len(df) + 1)
                st.dataframe(df.style.hide(axis="index"))


else:
    LOGGER.debug("FormSubmitter:search_form-Search is not True")


st.divider()
footer = """<style>
a:link , a:visited{
    color: grey;
    background-color: transparent;
    text-decoration: underline;
}

a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: grey;
    background-color: black;
    text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='text-align: center;' href="https://www.hudarashid.com/" target="_blank">Huda Rashid</a>. Found bugs? Report here at <a style='text-align: center;' href="https://github.com/hudarashid/lyrics_analysis/issues" target="_blank">Github</a>.</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
