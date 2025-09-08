# Test for language detection API
# This test will check if the language detection API is working correctly

def test_language_detection(api_client):
    response = api_client.post("/detect_language", json={"text": "Hello, world!"})
    assert response.status_code == 200
    assert response.json() == {"language": "en"}