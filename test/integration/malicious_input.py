# Test for malicious input handling
# This test will check if the API can handle malicious input without crashing

def test_malicious_input_xss(api_client):
    response = api_client.post("/classify_intent", json={"text": "<script>alert('xss')</script>"})
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid input"}


def test_malicious_input_sql_injection(api_client):
    response = api_client.post("/classify_intent", json={"text": "'; DROP TABLE users; --"})
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid input"}