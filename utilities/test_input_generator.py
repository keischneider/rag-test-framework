import json


def generate_test_input(eval_type, input_amount=10):
    """
    Depending on the evaluation type, generates test input for chatbot evaluation.

    Returns:
        JSONL with test input for evaluation. 
    """
    return json.dumps({
        "query": "<user_query>",
        "ground_truth": "<ground_truth>"
    })