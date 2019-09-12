# this is a module created to handle spotify/spotipy tasks
import sys
import spotipy
from spotipy import util as util
from polyjamoury.app.config import username, scope, client_id, client_secret_id, redirect_uri

# sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret_id, redirect_uri,
#         scope=scope, cache_path=".cache-" + username )
# code = sp_oauth.parse_response_code("https://www.google.com/?code=AQAi0EuThN4WJdi40tStrneACvx580y80vEm---ZxOLfzOSeNe98DzxbbKIu0G0t5nA9dkUsyUPr6g4Jhy3fkqvS651bWozv5f-774oQ1IwEZrsIi9SqRGpLkiPzfrZ-0RaJGoBDB7pZjzR7tehj-Oucd4whyWTYd1Dlqx95_KLF9anzAf_t66aPQU3w_5uJvNTU7sNfOD6gS-zjVLJ0caZW1J-lvYgcf-Ny9dIvba1I64tGqzXOwm0TS4PJaca1osu6zwinyFk2L0LZfNtieyC3JX_XlQ")
# print(code)
# token_info = sp_oauth.get_access_token(code)
#
# token = token_info['access_token']

token = util.prompt_for_user_token(username, scope, client_id, client_secret_id, redirect_uri)

try:
    spotify = spotipy.Spotify(auth=token)
    user = spotify.current_user()
    user_id = user['id']
# prints the type of exception error and exits the program if connection
except Exception as e:
    print(type(e))
    sys.exit('Cannot connect to spotify')


def get_recent50():
    return spotify.current_user_saved_tracks(50, 0)


def get_next_50():
    return spotify.current_user_saved_tracks(50, 49)


def playlist_create(name):
    return spotify.user_playlist_create(user_id, name)








if __name__ == '__main__':
    pass


def add_tracks_to_playlist(pl_id, tracks):
    return spotify.user_playlist_add_tracks(user_id, pl_id, tracks)