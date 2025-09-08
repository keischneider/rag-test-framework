# Test for entity extraction API
# This test will check if the entity extraction API is working correctly

def test_entity_extraction(api_client):
    response = api_client.post("/extract_entities", json={"text": "Show me all transactions from McDonald's"})
    assert response.status_code == 200
    assert response.json() == {"entities": [{"type": "merchant", "value": "McDonald's"}, {"type": "action", "value": "show_transactions"}]}
