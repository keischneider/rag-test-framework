import json
import time
from fetcher import fetch_data
from test_data.ragas.formatter import format_json, split_markdown
from test_data.ragas.knowledge_graph_builder import build_kg, build_generator
from rdf_graph_builder import test_rdf_graph, test_json_path_query
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
    result = test_json_path_query()
    prompt = get_testdata_prompt_template(
        result,
        persona_characteristics="""A young, using slang bank customer who is seeking assistance with their account and transactions.""",
        scenarios="""1. Checking account balance
2. Transferring money between accounts
3. Disputing a transaction
4. Updating personal information
5. Applying for a loan""",
        example_format="""use JSONL format: {"input": "<user_input>", "output": "<expected_output>"}""",
        num_cases=5)
    response = query_llm(prompt)
    print(response)
    save_to_file(f'test_questions/{int(time.time())}.jsonl', response)
    pass

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


if __name__ == "__main__":
    __main__()