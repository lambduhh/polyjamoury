import json
import pprint
from typing import Any

from naga import get_in, fpartial, nil, get, append


def open_json_data(data):
    with open('data.json', 'w') as f: f.write(json.dumps(data, indent=2))


def get_track_uris(d: dict) -> list:
    # get_in returns the value in a nested associative structure,
    # where second arg is a sequence of keys.
    track_uri = get_in(d, ["track", "uri"], not_found=None)
    return track_uri


def get_artist_uris(d: dict) -> list:
    artist_uri = get_in(d, ["uri"], not_found=None)
    # artist_name = get_in(d, ["name"], not_found=None)
    return artist_uri


def list_to_string(l: list):
    str1 = ""
    for ele in l:
        str1 += ele
    return str1


def dict_hash(x):
    if isinstance(x, dict):
        return hash(tuple(sorted((k, dict_hash(v)) for k, v in x.items())))

    if isinstance(x, (list, tuple, set)):
        return hash(tuple(map(dict_hash, x)))

    if isinstance(x, (int, float, str)) or x is None:
        return hash(type(x))

    raise Exception(type(x))


def filter_d_hash(xs):
    res = []
    seen_types = set()
    for x in xs:
        if dict_hash(x) not in seen_types:
            res.append(type(x))
            seen_types.add(dict_hash(x))
    return res


def spec_out(x, prev: Any = nil):
    if isinstance(x, (int, float, str)) or x is None:
        if isinstance(prev, tuple):
            return (type(x),)
        if isinstance(prev, list):
            return [type(x)]
        if isinstance(prev, set):
            return {type(x)}
        if isinstance(prev, dict):
            return spec_out(x)
        if prev is nil:
            return type(x)
        if x is None:
            return None

    if isinstance(x, list):
        l = list(map(fpartial(spec_out, x), filter_d_hash(x)))
        if len(l) == 1:
            return [spec_out(x[0])]
        return l
    if isinstance(x, tuple):
        t = tuple(map(fpartial(spec_out, x), filter_d_hash(x)))
        if len(x) == 1:
            return [spec_out(x[0])]
        return t
    if isinstance(x, set):
        s = set(map(fpartial(spec_out, x), filter_d_hash(x)))
        if len(s) == 1:
            return {spec_out(x.pop())}
        return s
    if isinstance(x, dict):
        return {k: spec_out(v, x) for k, v in x.items()}

    if isinstance(x, type):
        return x

    raise Exception(x, (type(x), type(prev)))


if __name__ == '__main__':
    print(spec_out({'a': [1, 2, {'hi': 2}]}))

    pprint.pprint(spec_out(json.load(open('data.json'))))
