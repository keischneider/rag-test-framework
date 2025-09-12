import json
from fetcher import fetch_data
from formatter import format_json, split_markdown
from knowledge_graph_builder import build_kg, build_generator


# A plan to create knowledge-graph-based context-providing prompt for an LLM to generate a testset:
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
    pass


def custom_testset_gen_pipeline():
    pass


def ragas_testset_gen_pipeline():
    data = json.loads(fetch_data())
    text = format_json(data)
    sections = split_markdown(text)
    kg_name = build_kg(sections)
    generator, distribution = build_generator(kg_name)
    testset = generator.generate(testset_size=5)
    testset.to_jsonl("testset.jsonl")


if __name__ == "__main__":
    __main__()