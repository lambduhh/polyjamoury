from polyjamoury.app.spot import get_one_track, audio_analysis, audio_features, get_saved_artists, get_artist_top_tracks
from polyjamoury.app.utils import get_track_uris, list_to_string, get_artist_uris
from collections import Counter
import json
from naga import mapv, append


def get_all_saved_artists():
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


def audio_features_all_saved():
    saved_artists = get_all_saved_artists()
    saved_artist_uri = set(mapv(get_artist_uris, saved_artists))
    # 91 different top saved artists
    ttrack_database = []
    for artist in saved_artist_uri:
        all_artist_top_songs = get_artist_top_tracks(artist)['tracks']
        for song in all_artist_top_songs:
          ttrack_database.append(song['uri'])
    return ttrack_database


if __name__ == '__main__':
    top_artist_top_tracks = audio_features_all_saved()
    # print(one_track_audio_features())
    # artists = saved_artists
    with open('top_artist_top_track.json', 'w') as f: f.write(json.dumps(top_artist_top_tracks, indent=2))
