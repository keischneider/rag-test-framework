import json
import time
from test_data.utils import fetch_data, save_to_file, json_to_list
from test_data.graph_builder import convert_to_triples_from
from test_data.llm_client import query_llm
from test_data.prompt_controller import get_testdata_prompt_template

# Plan 🧭
# create your fist custom evaluator for relevancy
# think of a usual pipeline from test data generation to evaluation


def __main__():
    custom_test_dataset_gen_pipeline()


def custom_test_dataset_gen_pipeline():
    json_data = json.loads(fetch_data('test_data/prompt_configuration_resources/test_user.json'))
    context = convert_to_triples_from(json_data)
    persona_json = json.loads(fetch_data('test_data/prompt_configuration_resources/personas.json'))[7]
    persona = '\n'.join(json_to_list(persona_json))
    scenarios_json = json.loads(fetch_data('test_data/prompt_configuration_resources/scenarios.json'))
    scenarios = '\n'.join([scenario['short_description'] for scenario in scenarios_json])
    output_format_json = json.loads(fetch_data('test_data/prompt_configuration_resources/output_formats.json'))
    output_format = ', '.join(json_to_list(output_format_json[1]))
    prompt = get_testdata_prompt_template(context, persona, scenarios, output_format)
    response = query_llm(prompt)
    print(response)
    save_to_file(f'test_data/test_questions/{int(time.time())}.jsonl', response)


# run with python -m test_data.test_data_gen
if __name__ == "__main__":
    __main__()