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
    text += "\n".join(json_to_list(data.get("knowledge_base")))
    text += "\n\nTransactions\n"
    for t in data.get("transactions"):
        text += "\n".join(json_to_list(t))
        text += "\n\n"
    return text


def split_markdown(text):
    pattern = r'Knowledge base|Transactions'
    matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
    sections = []
    for i, match in enumerate(matches):
        header = text[match.start():match.end()].strip()
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        section_text = text[start:end].strip()
        sections.append((header, section_text))
    return sections