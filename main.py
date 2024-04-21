from spotipy.oauth2 import SpotifyPKCE

from spotify import Spotify

# App credentials and permissions
CLIENT_ID = "552bcbe4f7ac4c1ea24d91ae0e9704ac"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "playlist-modify-public playlist-modify-private ugc-image-upload"


def main():
    auth_manager = SpotifyPKCE(CLIENT_ID, REDIRECT_URI, scope=SCOPE)
    spotify = Spotify(auth_manager=auth_manager)
    
    username = spotify.current_user()["display_name"]
    user_id = spotify.current_user()["id"]
    
    print(f"Hi {username}, Welcome To Makify\n")
    print("Select an option:\n- (1) Sort original playlist\n- (2) Clone and sort playlist")
    
    while True:
        option = int(input("> "))
        if option==1 or option==2:
            break
        print("Select a valid option")
    
    playlist_id = input("\nEnter the playlist ID: ")
    
    if option==1:
        spotify.sort_playlist(playlist_id, "artist, release_date, track_number")
    else:
        cloned_playlist = spotify.clone_playlist(playlist_id, user_id)
        spotify.sort_playlist(cloned_playlist["id"], "artist, release_date, track_number2")
    
    print("\nThe playlist has been ordered susefully")


if __name__ == "__main__":
    main()
