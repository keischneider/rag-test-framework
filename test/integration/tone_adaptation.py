# Test for tone adaptation
# This test will check if the API can adapt its tone based on user input

def test_tone_adaptation(api_client):
    response = api_client.post("/tone_adaptation", json={"text": "I lost a few grand but no idea where they are"})
    # response = I lost a few thousand dollars and don't know where and when.
    semantic_similarity_score = api_client.get_semantic_similarity_score(response.json(), {"text": "I lost a few thousand dollars and don't know where and when."})
    assert semantic_similarity_score > 0.9
