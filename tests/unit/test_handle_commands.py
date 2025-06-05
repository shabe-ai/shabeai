from app import handle
import uuid, types

def dummy_user():
    return {"id": str(uuid.uuid4())}

def test_add_account(tmp_path):
    resp = handle("add account globex", dummy_user())
    assert "globex" in resp.lower()

def test_bad_stage(tmp_path):
    bad = handle("set stage of bob@foo.com to nonsense", dummy_user())
    assert "unknown stage" in bad.lower() 