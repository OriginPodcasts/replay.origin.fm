from importlib import import_module


FINDERS = (
    'replay.directories.finders.apple',
    'replay.directories.finders.web'
)


def find(url):
    for finder in [import_module(m) for m in FINDERS]:
        found = finder.find(url)
        if found is not False and found is not None:
            return found

    return url
