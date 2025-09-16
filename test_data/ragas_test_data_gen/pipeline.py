import json
from test_data.utils import fetch_data
from ragas_test_data_gen.formatter import format_json, split_markdown
from ragas_test_data_gen.knowledge_graph_builder import build_kg, build_generator


def ragas_test_dataset_gen_pipeline():
    data = json.loads(fetch_data())
    text = format_json(data)
    sections = split_markdown(text)
    kg_name = build_kg(sections)
    generator, distribution = build_generator(kg_name)
    testset = generator.generate(testset_size=5)
    testset.to_jsonl("testset.jsonl")