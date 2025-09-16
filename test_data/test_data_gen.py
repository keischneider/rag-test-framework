import json
import time
from fetcher import fetch_data
from ragas_test_data_gen.formatter import format_json, split_markdown
from ragas_test_data_gen.knowledge_graph_builder import build_kg, build_generator
from rdf_graph_builder import convert_to_triples_from
from llm_client import query_llm
from prompt_controller import get_testdata_prompt_template

# Plan 🧭
# convert transaction history into RDF triples
# extend Personas
# create different scenarios (e.g. account management, transaction history, fraud detection, customer support, loan applications, investment advice, etc.)
# create different output formats (depending on evaluation input)
# create scenarios that query single, multi-hop, and mixed queries
# create scenarios that require different levels of specificity (high-level, detailed, technical, etc.)


def __main__():
    custom_test_dataset_gen_pipeline()
    pass


def custom_test_dataset_gen_pipeline():
    json_data = json.loads(fetch_data())
    context = convert_to_triples_from(json_data)
    persona_json = json.loads(fetch_data('prompt_configuration_resources/personas.json'))[0]
    persona = '\n'.join(json_to_list(persona_json))
    scenarios_json = json.loads(fetch_data('prompt_configuration_resources/scenarios.json'))
    scenarios = '\n'.join([scenario['short_description'] for scenario in scenarios_json])
    output_format_json = json.loads(fetch_data('prompt_configuration_resources/output_formats.json'))
    output_format = ', '.join(json_to_list(output_format_json[0]))
    prompt = get_testdata_prompt_template(context, persona, scenarios, output_format)
    response = query_llm(prompt)
    print(response)
    save_to_file(f'test_questions/{int(time.time())}.jsonl', response)


# raw version
def ragas_test_dataset_gen_pipeline():
    data = json.loads(fetch_data())
    text = format_json(data)
    sections = split_markdown(text)
    kg_name = build_kg(sections)
    generator, distribution = build_generator(kg_name)
    testset = generator.generate(testset_size=5)
    testset.to_jsonl("testset.jsonl")


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


if __name__ == "__main__":
    __main__()