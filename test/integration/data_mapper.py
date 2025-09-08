# DB retrieved data being mapped into final output format

def map_db_data_to_output_format(api_client):
    db_response = api_client.post("/get_transactions", json={"transaction_id": 123})
    # db_response = 1250.75 USD
    # Example mapping logic
    final_output = api_client.map_to_response_format(db_response.json())
    # output = $1,205.75
    assert final_output == db_response
