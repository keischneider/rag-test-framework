import jsonschema


schema = {
    "type": "object",
    "properties": {
        "user_query": {"type": "string"},
        "intent": {"type": "string"},
        "extracted_entities": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["user_query", "intent", "extracted_entities"]
}

data = {"user_query": "What is my account balance?", "intent": "check_balance", "extracted_entities": []}

jsonschema.validate(instance=data, schema=schema)