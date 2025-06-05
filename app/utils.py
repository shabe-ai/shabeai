import json
import uuid
import datetime

def to_json_safe(obj):
    """
    JSON-encode anything SQLModel .dict() returns.
    Falls back to str() for non-serialisable types like UUID, datetime.
    """
    return json.loads(json.dumps(obj, default=_fallback))

def _fallback(o):
    if isinstance(o, (uuid.UUID,)):
        return str(o)
    if isinstance(o, (datetime.datetime, datetime.date)):
        return o.isoformat()
    # add more if needed
    return str(o) 