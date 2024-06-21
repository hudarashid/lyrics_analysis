import json
import os
import re
import logging
from collections import Counter, defaultdict

import requests
from dotenv import load_dotenv
from lingua import Language, LanguageDetectorBuilder
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from spotify_service import SpotifyService
from streamlit.logger import get_logger


LOGGER = get_logger(__file__)
LOGGER.setLevel(logging.DEBUG)

load_dotenv()

USER_AGENT = os.getenv("USER_AGENT")
APP_PLATFORM = os.getenv("APP_PLATFORM")
SP_DC = os.getenv("SP_DC")
SP_KEY = os.getenv("SP_KEY")
LYRICS_URL = os.getenv("LYRICS_URL")


class LyricsService:
    def get_lyrics(self, track_id: str):
        access = SpotifyService.get_access(SP_DC, SP_KEY)
        url = LYRICS_URL + f"{track_id}"

        querystring = {"format": "json", "vocalRemoval": "false"}
        headers = {
            "User-Agent": USER_AGENT,
            "App-Platform": APP_PLATFORM,
            "Authorization": f"Bearer {access}",
        }

        try:

            response = requests.get(url, headers=headers, params=querystring)
            data = response.content.decode("utf-8")
            result = json.loads(data)

            return result

        except Exception as ex:
            LOGGER.debug(f"No lyrics found. Exception: {ex}")
            return

    def combined_lyrics(self, lyrics_response: object) -> dict:
        # TODO: return isRtlLanguage=True (arabic)
        lyric_dict = defaultdict(str)

        for index, line in enumerate(lyrics_response["lyrics"]["lines"]):
            words = line["words"]
            if words and words != "♪":  # Check if words is not empty
                lyric_dict[str(index)] = words

        return lyric_dict

    def find_repeated_phrases(self, lyrics: dict):
        phrase_count = defaultdict(int)

        # Count occurrences of each phrase
        for key, phrase in lyrics.items():
            phrase_count[phrase.lower()] += 1

        # Find phrases that are repeated
        repeated_phrases = {
            phrase: count for phrase, count in phrase_count.items() if count > 1
        }

        sorted_repeated_phrases = sorted(
            repeated_phrases.items(), key=lambda item: item[1], reverse=True
        )

        return phrase_count, sorted_repeated_phrases

    def count_most_common(
        self, formatted_lyrics
    ) -> tuple[int, list[tuple[str, int]], dict[str, int]]:
        # Split the string by commas, parentheses, question marks, double quotes, exclamation marks, spaces
        words_list = re.split(r'[,"\s()\?!]+', formatted_lyrics)

        count = len(words_list)

        words_list = [word.lower() for word in words_list if word]
        counter = Counter(words_list).most_common(10)
        LOGGER.debug(f"Word counter: {counter}")

        # Regular expressions to detect Korean, Chinese, and Japanese characters
        korean_pattern = re.compile(r"[\uac00-\ud7af]")
        chinese_pattern = re.compile(r"[\u4e00-\u9fff]")
        japanese_pattern = re.compile(r"[\u3040-\u309f\u30a0-\u30ff]")

        # Find all Korean, Chinese, and Japanese characters in the formatted_lyrics
        korean_chars = korean_pattern.findall(" ".join(words_list))
        chinese_chars = chinese_pattern.findall(formatted_lyrics)
        japanese_chars = japanese_pattern.findall(formatted_lyrics)

        # Count the number of Korean, Chinese, and Japanese characters
        korean_char_count = len(korean_chars)
        chinese_char_count = len(chinese_chars)
        japanese_char_count = len(japanese_chars)

        # Create a dictionary to store counts and labels
        char_counts = {
            "Korean": korean_char_count,
            "Chinese": chinese_char_count,
            "Japanese": japanese_char_count,
        }

        # Filter out languages with zero counts
        char_counts = {k: v for k, v in char_counts.items() if v > 0}

        return count, counter, char_counts

    def create_word_cloud(self, word_count):
        word_freq = dict(word_count)

        # "\n".join(combined_lyrics.values())

        # Generate word cloud
        wordcloud = WordCloud(
            font_path="AppleGothic.ttf",
            stopwords=None,
            width=800,
            height=400,
            background_color="white",
            regexp=r"[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff\uac00-\ud7af]+",
        ).generate_from_frequencies(word_freq)

        # Display the word cloud using matplotlib
        fig, ax = plt.subplots()
        ax.imshow(wordcloud)
        ax.axis("off")

        return fig

    def detect_language(self, formatted_lyrics):
        languages = [Language.ENGLISH, Language.KOREAN]
        detector = LanguageDetectorBuilder.from_all_languages().build()

        sentence = formatted_lyrics.replace("\n", " ")
        print(f"\n\n ==>> sentence: {sentence}")

        for result in detector.detect_multiple_languages_of(sentence):
            print(
                f"{result.language.name}: '{sentence[result.start_index:result.end_index]}'"
            )

        return


if __name__ == "__main__":
    lyric_service = LyricsService()
