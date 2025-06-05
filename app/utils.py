import json
import uuid
import datetime

def to_uuid(value: str | uuid.UUID) -> uuid.UUID:
    """
    Return a real UUID object.

    * If `value` already is / looks like a UUID -> use it as-is.
    * Otherwise derive a stable UUID from the input string so tests that
      pass in random tokens still work.
    """
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(str(value))
    except ValueError:
        # Stable, namespaced UUID based on arbitrary string
        return uuid.uuid5(uuid.NAMESPACE_OID, str(value))

def to_json_safe(obj):
    """
    JSON-encode anything SQLModel .dict() returns.
    Falls back to str() for non-serialisable types like UUID, datetime.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, dict):
        return {k: to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_json_safe(x) for x in obj]
    return obj

def _fallback(o):
    if isinstance(o, (uuid.UUID,)):
        return str(o)
    if isinstance(o, (datetime.datetime, datetime.date)):
        return o.isoformat()
    # add more if needed
    return str(o) 