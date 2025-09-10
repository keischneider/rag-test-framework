import re


def json_to_list(data, prefix=""):
    result = []
    if isinstance(data, dict):
        for k, v in data.items():
            result.extend(json_to_list(v, f"{prefix}{k}:"))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            result.extend(json_to_list(v, f"{prefix}{i}: "))
    else:
        result.append(f"{prefix}{data}")
    return result


def format_json(data):
    text = ""
    text += "\n\nKnowledge base\n"
    text += "\n".join(json_to_list(data.get("knowledge_base"), "   "))
    text += "\n\nTransactions\n"
    for t in data.get("transactions"):
        text += "\n".join(json_to_list(t, "   "))
        text += "\n\n"
    return text


def split_markdown(text):
    # split by Headers using regex
    # store each chunks along with the header
    pass