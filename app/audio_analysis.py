from polyjamoury.app.spot import get_one_track, audio_analysis, audio_features, get_saved_artists
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
    saved_artist_uri = mapv(get_artist_uris, saved_artists)
    print(saved_artist_uri)
    print(Counter(saved_artist_uri))
    return data


if __name__ == '__main__':

    # print(one_track_audio_features())
    # artists = saved_artists
    # with open('artists.json', 'w') as f: f.write(json.dumps(artists, indent=2))
