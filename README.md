# [Song Lyrics Analysis](https://lyricsanalysis.streamlit.app/)

### Motivation
This project is inspired by a recent study indicating that song lyrics are becoming increasingly simpler and more repetitive. For more details, refer to the [Scientific American article](https://www.scientificamerican.com/article/song-lyrics-really-are-getting-simpler-and-more-repetitive-study-finds/).

As an English language learner, I often listen to English songs to enhance my language skills. I have observed that contemporary song lyrics tend to be simpler and more repetitive, aligning with the study's findings. Additionally, I am keen on learning German and Korean languages, which motivated me to develop this Streamlit project. It analyzes song lyrics, providing insights into word count, most repetitive words and phrases, and unique words appearing only once. This tool primarily supports lyrics in Latin scripts.

I have also included functionality for counting CJK (Chinese, Japanese, and Korean) characters, recognizing that some songs feature a mix of languages, such as "My Universe" by Coldplay and BTS. However, due to my limited experience with CJK languages, I cannot guarantee the accuracy of these analyses. Feedback on songs in CJK languages is welcome; please open issues in the GitHub repository for any suggestions or corrections.

### Further Improvements
- [ ] Implement language detection
- [ ] Calculate and display the percentage of each language based on word count for multilingual lyrics
- [ ] Increase the number of search results displayed beyond the current limit of 10
- [ ] Include additional song information (genre, album, release year)
- [ ] Develop unit tests

*This project utilizes the Spotify Web API, and the lyrics is based on Spotify's lyrics availability.*
