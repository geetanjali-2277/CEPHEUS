def play_music_on_youtube(song_name):
    """Play a song on YouTube.

    Tries to use pywhatkit.playonyt (which requires internet). If importing
    or calling pywhatkit fails (offline or DNS issues), falls back to
    opening a YouTube search in the user's default browser.
    """
    try:
        import pywhatkit as pw
        pw.playonyt(song_name)
        return True
    except Exception:
        # Fallback: open a YouTube search page for the song
        import webbrowser
        from urllib.parse import quote_plus

        query = quote_plus(song_name)
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        return False


