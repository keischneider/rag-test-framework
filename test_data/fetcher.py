def fetch_data(path="test_user.json"):
    # Simulate fetching data for a user
    with open(path, "r") as test_user:
        return test_user.read()