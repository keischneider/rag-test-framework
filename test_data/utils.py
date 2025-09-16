import json


def fetch_data(path):
    with open(path, "r") as f:
        return f.read()


def save_to_file(filename, content):
    with open(filename, "w") as f:
        if content is None:
            raise ValueError("Content to write is None. Check the response from the LLM.")
        if isinstance(content, (dict, list)):
            json.dump(content, f, indent=2)
        else:
            f.write(str(content))


def json_to_list(data, prefix=""):
    result = []
    if isinstance(data, dict):
        for k, v in data.items():
            result.extend(json_to_list(v, f"{prefix}{k}: "))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            result.extend(json_to_list(v, f"{prefix}{i}: "))
    else:
        result.append(f"{prefix}{data}")
    return result