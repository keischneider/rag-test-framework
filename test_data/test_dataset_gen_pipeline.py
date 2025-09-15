import json
import time
from fetcher import fetch_data
from formatter import format_json, split_markdown
from knowledge_graph_builder import build_kg, build_generator
from rdf_graph_builder import test_rdf_graph, test_json_path_query
from llm_client import query_llm
from prompt_controller import get_testdata_prompt_template

# A plan to create knowledge-graph-based context-providing prompt for an LLM to generate a testset:
# 9/15 update (a substiture for 1, 2 steps)
# define a sequence of query to knowledge base to get the necessary data in a structured way (e.g. SPARQL or JSONpath queries to get data for each account, for each card, for each personal info, etc.)
# convert the fetched data into a RDF-like triples
# 1. get raw JSON with all the data
# 2. Convert it into RDF triples
    # a. (optional) filter out unnecessary data
# 3. Convert RDF triples into "natural" triples for an LLM to process
# 4. Wrap the text sections into a prompt template to generate test dataset
    # 4.1. in the prompt template, define personas and scenarios
    # 4.2. define the expected output format and expected properties (JSONL)
    # 4.3. define the level of specificity
    # 4.4. define the minimum/maximum number of sources to be used (single, multihop queries)

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