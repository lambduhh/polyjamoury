from naga import append, mapv, get_in
from polyjamoury.app.spot import get_recent50, get_next_50, playlist_create, add_tracks_to_playlist


# this program finds the 100 tracks that were most recently 'saved' to spotify, and creates a playlist with them


def saved_tracks():
    recent50 = get_recent50()
    items_of_r50 = recent50['items']
    next50 = get_next_50()
    items_of_n50 = next50['items']
    all_100_tracks = append(items_of_r50, items_of_n50)
    return all_100_tracks


def get_track_uris(d: dict):
    # get_in returns the value in a nested associative structure,
    # where second arg is a sequence of keys.
    track_uri = get_in(d, ["track", "uri"], not_found=None)
    return track_uri


def create_playlist(name_of_playlist):
    playlist = playlist_create(name_of_playlist)
    playlist_id = playlist['id']
    return playlist_id


def make_playlist_of_last_100(name_of_playlist, tracks):
    # mapv = list(map())
    s_track_uri_data = mapv(get_track_uris, tracks)
    pl_id = create_playlist(name_of_playlist)
    add_tracks_to_playlist(pl_id, s_track_uri_data)
    return None


if __name__ == '__main__':
    all_tracks = saved_tracks()
    make_playlist_of_last_100("latest added jamzz 9/12/19", all_tracks)
