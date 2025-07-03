def test_list_leads(client, auth_headers, sample_lead):
    resp = client.get("/leads/", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1  # at least one lead
    assert data[0]["email"] == "test@example.com"
