import json
from fetcher import fetch_data
from formatter import format_json, split_markdown
from knowledge_graph_builder import build_kg, build_generator


# run the script with 
# cd test_data
# 'python testdata_pipeline.py'

# How do we configure personas?
# How do we configure Scenarios (queries)?

def __main__():
    data = json.loads(fetch_data())
    text = format_json(data)
    sections = split_markdown(text)
    # kg_name = build_kg(sections)
    generator, distribution = build_generator("knowledge_graph.json")
    testset = generator.generate(testset_size=5)
    testset.to_jsonl("testset.jsonl")


if __name__ == "__main__":
    __main__()