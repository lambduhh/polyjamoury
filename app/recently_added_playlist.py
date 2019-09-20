from naga import append, mapv
from polyjamoury.app.spot import get_recent50, get_next_50, add_tracks_to_playlist
from polyjamoury.app.utils import get_track_uris, create_playlist


# this program finds the 100 tracks that were most recently 'saved' to spotify, and creates a playlist with them


def saved_tracks() -> list:
    recent50 = get_recent50()
    items_of_r50 = recent50['items']
    next50 = get_next_50()
    items_of_n50 = next50['items']
    all_100_tracks = append(items_of_r50, items_of_n50)
    return all_100_tracks


def make_playlist_of_last_100(name_of_playlist, tracks):
    # mapv = list(map())
    s_track_uri_data = mapv(get_track_uris, tracks)
    pl_id = create_playlist(name_of_playlist)
    add_tracks_to_playlist(pl_id, s_track_uri_data)
    return None


if __name__ == '__main__':
    all_tracks = saved_tracks()
    # make_playlist_of_last_100("latest added jamzz 9/16/19", all_tracks)
    #TODO -auto delete previous playlist of the same name
