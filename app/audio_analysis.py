from app.spot import get_one_track, audio_features, get_saved_artists, \
    add_tracks_to_playlist, get_artist_top_tracks
from app.utils import get_track_uris, list_to_string, get_artist_uris, create_playlist
import json
from naga import mapv, append, get_in
from functools import partial


def get_all_fav_artists() -> list:
    st = get_saved_artists('short_term')
    stitems = st['items']
    mt = get_saved_artists('medium_term')
    mtitems = mt['items']
    lt = get_saved_artists('long_term')
    ltitems = lt['items']
    return append(stitems, mtitems, ltitems)


def one_track_audio_features():
    one_track = get_one_track()
    item = one_track["items"]
    uri_data = mapv(get_track_uris, item)
    uri_data_str = list_to_string(uri_data)
    data = audio_features(uri_data_str)
    return data


def audio_features_all_favs() -> list:
    fav_artists = get_all_fav_artists()
    saved_artist_uri = set(mapv(get_artist_uris, fav_artists))
    # 91 different top saved artists (9/16/19)
    ttrack_database = []
    for artist in saved_artist_uri:
        all_artist_top_songs = get_artist_top_tracks(artist)['tracks']
        for song in all_artist_top_songs:
            ttrack_database.append(song['uri'])
    # a database that is a list
    # of user's top artist's top tracks, 921 songs (9/16/19), 750 songs (10/11/19)
    return ttrack_database


colors = {"red": {"danceability": {"min": 0, 'max': .5},
                  "energy": {"min": .7, 'max': 1.0},
                  "acousticness": {"min": 0, 'max': .4},
                  "tempo": {"min": 65.0, 'max': 300.0},
                  "valence": {"min": 0, 'max': .45}
                  },
          "yellow": {"danceability": {"min": .45, 'max': 1.0},
                     "energy": {"min": .6, 'max': 1.0},
                     "acousticness": {"min": 0, 'max': .5},
                     "tempo": {"min": 60.0, 'max': 200.0},
                     "valence": {"min": .8, 'max': 1.0}
                     },
          "pink": {"danceability": {"min": .7, 'max': 1.0},
                   "energy": {"min": .25, 'max': .8},
                   "acousticness": {"min": 0, 'max': .5},
                   "tempo": {"min": 0, 'max': 150},
                   "valence": {"min": .5, 'max': .85},
                   },
          "green": {"danceability": {"min": .5, 'max': .7},
                    "energy": {"min": .2, 'max': .5},
                    "acousticness": {"min": .5, 'max': 1.0},
                    "tempo": {"min": 0.0, 'max': 180},
                    "valence": {"min": .35, 'max': .75}
                    },
          "blue": {"danceability": {"min": 0, 'max': .48},
                   "energy": {"min": 0, 'max': .5},
                   "acousticness": {"min": .2, 'max': .8},
                   "tempo": {"min": 0, 'max': 180},
                   "valence": {"min": 0, 'max': .5}
                   }}


def get_ssong_features(ssongs: list) -> dict:
    d_song_features = {}
    for song in ssongs:
        d_song_features[song] = audio_features(song)[0]
    return d_song_features


# predicate fn to get passed to (filter(partial(fn))
def is_song_color(color: dict, song: dict) -> bool:
    if not color["danceability"]["min"] <= song["danceability"] <= color["danceability"]["max"]:
        return False
    elif not color["energy"]["min"] <= song["energy"] <= color["energy"]["max"]:
        return False
    elif not color["acousticness"]["min"] <= song["acousticness"] <= color["acousticness"]["max"]:
        return False
    elif not color["tempo"]["min"] <= song["tempo"] <= color["tempo"]["max"]:
        return False
    elif not color["valence"]["min"] <= song["valence"] <= color["valence"]["max"]:
        return False
    else:
        return True


def get_song_features():
    with open('json_data/all_fav_songs_features.json') as f:
        all_fav_songs_features = json.load(f)
    return all_fav_songs_features


def create_color_data(color: str) -> list:
    all_fav_songs_features = get_song_features()
    colorsongs = list(filter(partial(is_song_color, colors[color]), all_fav_songs_features.values()))
    return colorsongs


def save_songs(colorsongs):
    with open('colorsongs.json', 'w') as f:
        f.write(json.dumps(colorsongs, indent=2))
    return colorsongs


def create_color_pl(colorsongs: list, title: str) -> None:
    pl_id = create_playlist(title)
    playlist = []
    for song in colorsongs:
        song_uris = get_artist_uris(song)
        playlist.append(song_uris)
    add_tracks_to_playlist(pl_id, playlist)
    return None


if __name__ == '__main__':
    # top_artist_top_tracks = audio_features_all_favs()
    # print(len(top_artist_top_tracks))
    colorsongs = create_color_data("")
    save_songs(colorsongs)
    # print(create_color_pl(colorsongs, "green"))
    # # yellow3 = one_track_audio_features()
    # with open('yellow3.json', 'w') as f: f.write(json.dumps(yellow3, indent=2))
