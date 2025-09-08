# Test for API selection
# This test will check if the correct API is selected based on the user query

def test_api_selection(api_client):
    response = api_client.post("/select_api", json={"query": "Show me all transactions from McDonald's"})
    assert response.status_code == 200
    assert response.json() == {"selected_api": "live_transaction_api"}

def test_api_selection_2(api_client):
    response = api_client.post("/select_api", json={"query": "I forgot my PIN"})
    assert response.status_code == 200
    assert response.json() == {"selected_api": "knowledge_base_retrieval"}