# Test for intent classification LLM

def test_intent_classification(api_client):
    response = api_client.post("/classify_intent", json={"text": "Show me all transactions from McDonald's"})
    assert response.status_code == 200
    assert response.json() == {"intent": "show_transactions"}