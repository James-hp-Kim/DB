"""Shared serialization and evidence fingerprints; no external dependencies."""
import hashlib
import json

VERSION = '2.5.2'


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def digest(path):
    result = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()
