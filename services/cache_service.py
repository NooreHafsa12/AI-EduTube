import uuid

VIDEO_CACHE = {}


def save_video_data(session, data):
    cache_id = session.get("cache_id")

    if not cache_id:
        cache_id = str(uuid.uuid4())
        session["cache_id"] = cache_id

    VIDEO_CACHE[cache_id] = data
    session.modified = True


def get_video_data(session):
    cache_id = session.get("cache_id")

    if not cache_id:
        return None

    return VIDEO_CACHE.get(cache_id)


def clear_video_data(session):
    cache_id = session.get("cache_id")

    if cache_id and cache_id in VIDEO_CACHE:
        del VIDEO_CACHE[cache_id]

    session.pop("cache_id", None)
    session.modified = True