# this is a module created to handle spotify/spotipy tasks
import sys
import spotipy
from spotipy import util as util, oauth2
from polyjamoury.app.config import username, scope, client_id, client_secret_id, redirect_uri


###
#
###

def reauth(conn_str: str) -> "token":
    """Reauthorize spotify app.
    :param conn_str: "https://www.google.com/?code=AQBBH8rayjMv1yRGBQFMZK5jJkMEWxJi5HMuK_qZubCj71HoMzMD0mH_v8WVGEd3kuYsTw7TB0uKwlmTVmUz3q8xcSwX6ppHHrP0aykTqtTHlLePVsXuvCdH8MsZjVo6E0fXSEmN4xwCK5MXIDVu6AAn2EzxdlgtdbdKrBXSzR9Tt--B19vYkOPTtteTGF1bmzHUTBGSC-P-pH3nRvtqA4v90LlEMFFcMKUPfMKKOpAxNtGGLNhqc4opynVIJ_Gk3tTLbbrpKdYY_Ftq56gf6RTh9YWGTg"
    :type conn_str: str
    :return: token
    """
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret_id, redirect_uri,
                                   scope=scope, cache_path=".cache-" + username)
    code = sp_oauth.parse_response_code(conn_str)
    print(code)
    token_info = sp_oauth.get_access_token(code)

    token = token_info['access_token']
    return token


try:
    token = util.prompt_for_user_token(username, scope, client_id, client_secret_id, redirect_uri)
except Exception as e:
    token = None
    raise Exception("Unable to obtain token")

try:
    spotify = spotipy.Spotify(auth=token)
    user = spotify.current_user()
    user_id = user['id']
# prints the type of exception error and exits the program if connection
except Exception as e:
    print(type(e))
    sys.exit('Cannot connect to spotify')


def get_one_track():
    return spotify.current_user_saved_tracks(1, 0)


def get_recent50():
    return spotify.current_user_saved_tracks(50, 0)


def get_next_50():
    return spotify.current_user_saved_tracks(50, 49)


def get_saved_artists(time_range):
    return spotify.current_user_top_artists(50, time_range=time_range)


def playlist_create(name):
    return spotify.user_playlist_create(user_id, name)


def add_tracks_to_playlist(pl_id, tracks):
    return spotify.user_playlist_add_tracks(user_id, pl_id, tracks)


def audio_analysis(track_id):
    return spotify.audio_analysis(track_id)


def audio_features(tracks):
    return spotify.audio_features(tracks)


def get_artist_top_tracks(artist_id):
    return spotify.artist_top_tracks(artist_id, country='US')

#
if __name__ == '__main__':
    reauth(
        "https://www.google.com/?code=AQBBH8rayjMv1yRGBQFMZK5jJkMEWxJi5HMuK_qZubCj71HoMzMD0mH_v8WVGEd3kuYsTw7TB0uKwlmTVmUz3q8xcSwX6ppHHrP0aykTqtTHlLePVsXuvCdH8MsZjVo6E0fXSEmN4xwCK5MXIDVu6AAn2EzxdlgtdbdKrBXSzR9Tt--B19vYkOPTtteTGF1bmzHUTBGSC-P-pH3nRvtqA4v90LlEMFFcMKUPfMKKOpAxNtGGLNhqc4opynVIJ_Gk3tTLbbrpKdYY_Ftq56gf6RTh9YWGTg")
