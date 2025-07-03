def test_list_leads(client, auth_headers, sample_lead):
    resp = client.get("/leads/", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1  # at least one lead
    emails = [lead["email"] for lead in data]
    assert sample_lead.email in emails
