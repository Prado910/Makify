import base64

import requests
import spotipy


class Spotify(spotipy.Spotify):
    def __init__(self, auth=None, oauth_manager=None, auth_manager=None):
        super().__init__(auth, oauth_manager, auth_manager)

    def clone_playlist(self, playlist: dict, user_id: str) -> dict:
        """Creates a new playlist equal to the original playlist.

        Args:
            playlist (dict): The original playlist.
            user_id (str): The id of the user.

        Returns:
            dict: The new playlist.
        """
        name = playlist["name"] + " (Makify)"
        new_playlist = self.user_playlist_create(
            user_id, name, playlist["public"], playlist["description"]
        )

        img = requests.get(playlist["images"][0]["url"]).content
        self.change_playlist_image(new_playlist, img)

        return new_playlist

    def change_playlist_image(self, playlist: dict, img: bytes):
        """Changes the cover image of a playlist.

        Args:
            playlist (dict): The playlist dict.
            img (bytes):  The image bytes to set as the cover image.
        """
        img_b64 = base64.b64encode(img).decode("utf-8")
        self.playlist_upload_cover_image(playlist["id"], img_b64)

    def get_playlist_tracks(self, playlist_id: str) -> list:
        """Get a list of all tracks in a playlist.

        Args:
            playlist_id (str): The id of the playlist.

        Returns:
            list: A list of all tracks in the playlist.
        """
        playlist_tracks = self.playlist_tracks(playlist_id)
        tracks = list()

        while True:
            for item in playlist_tracks["items"]:
                tracks.append(item["track"])

            if playlist_tracks["next"]:
                playlist_tracks = self.next(playlist_tracks)
            else:
                break

        for track in tracks:
            track["artists"][0]["name"] = track["artists"][0]["name"].lower()

        return tracks

    def sort_tracks(self, tracks: list) -> list:
        """Sort a list of tracks.

        Args:
            tracks (list): A list of tracks to sort.

        Returns:
            list: The sorted list of tracks.
        """
        sorted_tracks = sorted(
            tracks,
            key=lambda x: (
                x["artists"][0]["name"],
                x["album"]["release_date"],
                x["album"]["name"],
                x["disc_number"],
                x["track_number"],
            ),
        )
        return sorted_tracks

    def get_track_uris(self, tracks: list) -> list:
        """Get a list of Spotify URIs for a list of tracks.

        Args:
            tracks (list): A list of tracks.

        Returns:
            list: A list of Spotify URIs.
        """
        return [track["uri"] for track in tracks]

    def add_tracks_to_playlist(self, playlist_id: str, uris: list):
        """Add a list of track URIs to a playlist.

        Args:
            playlist_id (str): The id of the playlist
            uris (list): A list of track URIs.
        """
        while True:
            if len(uris) > 100:
                self.playlist_add_items(playlist_id, uris[:100])
                uris = uris[100:]
            else:
                self.playlist_add_items(playlist_id, uris)
                break
