from spotipy.oauth2 import SpotifyPKCE

from spotify import Spotify

# App credentials and permissions
CLIENT_ID = "552bcbe4f7ac4c1ea24d91ae0e9704ac"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "playlist-modify-public playlist-modify-private ugc-image-upload"


def main():
    user_id = input("Enter your user ID: ")
    playlist_id = input("Enter the playlist ID: ")

    auth_manager = SpotifyPKCE(CLIENT_ID, REDIRECT_URI, scope=SCOPE)
    spotify = Spotify(auth_manager=auth_manager)

    playlist = spotify.playlist(playlist_id)
    new_playlist = spotify.clone_playlist(playlist, user_id)

    tracks = spotify.get_playlist_tracks(playlist_id)
    sorted_tracks = spotify.sort_tracks(tracks)
    track_uris = spotify.get_track_uris(sorted_tracks)

    spotify.add_tracks_to_playlist(new_playlist["id"], track_uris)


if __name__ == "__main__":
    main()
