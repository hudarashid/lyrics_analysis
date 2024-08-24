CONSTRUCT_QUERY_TEST_CASES = [
    (
        {
            "track": "Bohemian Rhapsody",
            "artist": "Queen",
            "album": "A Night at the Opera",
        },
        "track:Bohemian Rhapsody artist:Queen album:A Night at the Opera",
    ),
    ({"track": "Imagine", "artist": "John Lennon"}, "track:Imagine artist:John Lennon"),
    (
        {"artist": "The Beatles", "album": "Abbey Road"},
        "artist:The Beatles album:Abbey Road",
    ),
    ({"track": "Yesterday"}, "track:Yesterday"),
    ({}, ""),
]
