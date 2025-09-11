def fetch_data():
    # Simulate fetching data for a user
    with open("test_user.json", "r") as test_user:
        return test_user.read()