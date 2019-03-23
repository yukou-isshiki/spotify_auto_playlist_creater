import spotipy
import spotipy.util as util

class Spotify_token:
    def __init__(self, username):
        self.username = username
        self.scope = 'playlist-modify-public user-read-playback-state user-modify-playback-state'
        #self.scope = 'user-modify-playback-state'

    def set(self):
        token = util.prompt_for_user_token(self.username, self.scope)
        return token