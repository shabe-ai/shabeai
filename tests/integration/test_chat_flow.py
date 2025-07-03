# TODO: This test is for future chat functionality that hasn't been implemented yet
# from app import handle

# def test_full_flow(client, demo_user):
#     ctx_user = {"id": demo_user["token"].split('.')[0]}   # quick fake
#     # 1 create account
#     assert "created" in handle("add account hr inc", ctx_user).lower()
#     # 2 add + attach lead
#     handle("add lead sam@hrinc.com", ctx_user)
#     res = handle("attach lead sam@hrinc.com to hr inc", ctx_user)
#     assert "attached" in res.lower()
#     # 3 funnel report returns a plotly figure object
#     fig = handle("reports funnel", ctx_user)
#     from plotly.graph_objs import Figure
#     assert isinstance(fig, Figure) 

def test_placeholder():
    """Placeholder test until chat functionality is implemented"""
    assert True 