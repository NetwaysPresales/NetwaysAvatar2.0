def fetch_user_from_db(user_id: str):
    """
    Fetches user data from the database.
    Returns a dictionary with user details if found, else None.
    """
    # Simulated database query
    mock_db = {
        "user_1": {
            "name": "Alice Example",
            "job": "Software Engineer",
            "past_conversations": [
                {"id": "conv1", "title": "Chat from Jan 1", "summary": "Summary of chat 1"},
                {"id": "conv2", "title": "Chat from Feb 5", "summary": "Summary of chat 2"}
            ]
        },
        "user_2": {
            "name": "Bob AI",
            "job": "Data Scientist",
            "past_conversations": [
                {"id": "conv3", "title": "Research Chat", "summary": "Discussed AI papers"},
                {"id": "conv4", "title": "ML Talk", "summary": "Spoke about deep learning"}
            ]
        }
    }

    return mock_db.get(user_id, None)
