import base64

import requests
import spotipy

class Spotify(spotipy.Spotify):
    def __init__(self, auth=None, oauth_manager=None, auth_manager=None):
        super().__init__(auth, oauth_manager, auth_manager)

    def clone_playlist(self, playlist_id: str, user_id: str) -> dict:
        """Create a new playlist equal to the original playlist.

        Args:
            playlist (str): The original playlist id.
            user_id (str): The id of the user.

        Returns:
            dict: The new playlist.
        """
        playlist = self.playlist(playlist_id)
        tracks = self.get_playlist_tracks(playlist_id)
        uris = self.get_track_uris(tracks)
        
        name = playlist["name"] + " (cloned by Makify)"
        
        new_playlist = self.user_playlist_create(
            user_id, name, playlist["public"], playlist["description"]
        )
        
        self.add_tracks_to_playlist(new_playlist["id"], uris)
        
        img = requests.get(playlist["images"][0]["url"]).content
        self.change_playlist_image(new_playlist["id"], img)

        return new_playlist

    def change_playlist_image(self, playlist_id: str, img: bytes):
        """Change the cover image of a playlist.

        Args:
            playlist_id (str): The id of the playlist.
            img (bytes):  The image bytes to set as the cover image.
        """
        img_b64 = base64.b64encode(img).decode("utf-8")
        self.playlist_upload_cover_image(playlist_id, img_b64)

    def get_playlist_tracks(self, playlist_id: str) -> list:
        """Get a list of all tracks in a playlist.

        Args:
            playlist_id (str): The id of the playlist.

        Returns:
            list: A list of all tracks in the playlist.
        """
        playlist_tracks = self.playlist_tracks(playlist_id)  # Get first 100 playlist tracks
        tracks = list()

        while True:
            for item in playlist_tracks["items"]:
                tracks.append(item["track"])

            if playlist_tracks["next"]:
                playlist_tracks = self.next(playlist_tracks)  # Next 100 tracks
            else:
                break

        for track in tracks:
            track["artists"][0]["name"] = track["artists"][0]["name"].lower()

        return tracks

    def sort_tracks(self, tracks: list, sort_by: str) -> list:
        """Sort a list of tracks.

        Args:
            tracks (list): A list of tracks to sort.
            sort_by (str): A comma-separated string of keys to sort the tracks by, in order of priority. Valid keys are:
                           "name", "artist", "album_name", "release_date", "track_number".

        Returns:
            list: The sorted list of tracks.
        """
        key_funcs = list()
        for key in sort_by.replace(" ", "").split(","):
            if key == "name":
                key_funcs.append(lambda x: x["name"])
            elif key == "artist":
                key_funcs.append(lambda x: x["album"]["artists"][0]["name"])
            elif key == "album_name":
                key_funcs.append(lambda x: x["album"]["name"])
            elif key == "release_date":
                key_funcs.append(lambda x: x["album"]["release_date"])
            elif key == "track_number":
                key_funcs.append(lambda x: (x["disc_number"], x["track_number"]))

        sorted_tracks = sorted(
            tracks, key=lambda x: tuple(key_func(x) for key_func in key_funcs)
        )
        return sorted_tracks

    def get_track_ids(self, tracks: list) -> list:
        return [track["id"] for track in tracks]

    def get_track_uris(self, tracks: list) -> list:
        return [track["uri"] for track in tracks]

    def add_tracks_to_playlist(self, playlist_id: str, uris: list):
        """Add a list of tracks to a playlist.

        Args:
            playlist_id (str): The id of the playlist.
            uris (list): A list of track URIs.
        """
        while True:
            if len(uris) > 100:
                self.playlist_add_items(playlist_id, uris[:100])
                uris = uris[100:]
            else:
                self.playlist_add_items(playlist_id, uris)
                break

    def remove_playlist_tracks(self, playlist_id: str, ids: list):
        """Remove a list of tracks from a playlist.

        Args:
            playlist_id (str): The id of the playlist.
            ids (list): A list of track IDs.
        """
        while True:
            if len(ids) > 100:
                self.playlist_remove_all_occurrences_of_items(playlist_id, ids[:100])
                ids = ids[100:]
            else:
                self.playlist_remove_all_occurrences_of_items(playlist_id, ids)
                break

    def sort_playlist(self, playlist_id: str, sort_by: str):
        """Sort the tracks of a playlist.

        Args:
            playlist_id (str): The id of the playlist.
            sort_by (str): A comma-separated string of keys to sort the tracks by, in order of priority. Valid keys are:
                           "name", "artist", "album_name", "release_date", "track_number".
        """

        tracks = self.get_playlist_tracks(playlist_id)
        sorted_tracks = self.sort_tracks(tracks, sort_by)
        track_ids = self.get_track_ids(sorted_tracks)
        track_uris = self.get_track_uris(sorted_tracks)

        self.remove_playlist_tracks(playlist_id, track_ids)
        self.add_tracks_to_playlist(playlist_id, track_uris)
