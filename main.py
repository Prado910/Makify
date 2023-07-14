from spotipy.oauth2 import SpotifyPKCE

from spotify import Spotify

# App credentials and permissions
CLIENT_ID = "552bcbe4f7ac4c1ea24d91ae0e9704ac"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "playlist-modify-public playlist-modify-private ugc-image-upload"


def main():
    auth_manager = SpotifyPKCE(CLIENT_ID, REDIRECT_URI, scope=SCOPE)
    spotify = Spotify(auth_manager=auth_manager)

    user_id = spotify.current_user()["id"]
    playlist_id = input("Enter the playlist ID: ")

    spotify.sort_playlist(playlist_id, "artist, release_date, track_number")


if __name__ == "__main__":
    main()
