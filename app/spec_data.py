import json
import pprint
from functools import partial

from naga import *
def spec_out(x, prev=nil):

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
        return list(map(fpartial(spec_out, x), x))
    if isinstance(x, tuple):
        return tuple(map(fpartial(spec_out, x), x))
    if isinstance(x, set):
        return set(map(fpartial(spec_out, x), x))
    if isinstance(x, dict):
        return {k: spec_out(v) for k, v in x.items()}


if __name__ == '__main__':

    print(spec_out({'a': [1, 2, {'hi': 2}]}))

    pprint.pprint(spec_out(json.load(open('data.json'))))