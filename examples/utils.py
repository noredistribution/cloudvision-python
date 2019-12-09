import json
from AerisRequester.codec import Path, FrozenDict


def pretty_print(dataDict):
    def default(obj):
        if isinstance(obj, Path):
            return obj._keys
        if isinstance(obj, (FrozenDict, dict)):
            return obj._dict
    print(json.dumps(
        dataDict, default=default, indent=4,
        sort_keys=True, separators=(",", ":")
    ))
