import json
import pytest
import os
from dotenv import load_dotenv
from utils.test_input_generator import generate_test_input
from utils.translator import translate
from e2e.groundedness import evaluate_groundedness
from e2e.relevance import evaluate_relevance
from utils.miscellanous import read
from utils.reporter import publish_report
from openai import OpenAI
from test_data.fetcher import fetch_data
from test_data.ragas_test_data_gen.formatter import format_json

load_dotenv()

# 1. We have 2 main "modes" of running evaluations. Either of these modes starts:
    # 1. Static mode - evaluates the model on the pre-generated and translated  input. Reusable test data that was proof-read and edited by humans
    #   and potentially become a part of regression suite.
        # 1.1. For test start user provides a path to input test data (e.g. /path/to/data/cz.json)
    # 2. Dynamic/Exploratory mode - evaluates the model on runtime-generated input. Allows for more testing randomness in the evaluation process.
        # 2.1. User provides just the set of languages (e.g. ["cz", "sk", "hu"])
        # 2.2. Input test data is generated
        # 2.3. The generated input is then translated into the target languages
# 2. The evaluation is performed on the input.
# 3. The evaluation outputs are then aggregated and reported.

# openai client setup:
    # response = OpenAI(api_key=os.getenv("OPENAI_API_KEY")).responses.create(
    #     model="gpt-5-mini",
    #     input="Write a one-sentence bedtime story about a unicorn."
    # )
    # print(response.output_text)


# run the test with 'PYTHONPATH=. pytest -s -m test'
@pytest.mark.test
def test_example():
    data = json.loads(fetch_data())
    text = format_json(data)
    # docs = split_markdown(text)
    # print(docs)


# Dynamic/Exploratory mode (runtime arguments)
@pytest.mark.dynamic
def test_dynamic(eval_type, langs):
    generated = generate_test_input(eval_type, 5)
    translated = translate(generated, langs)
    output = evaluate_groundedness(translated)
    publish_report(output)


# Dynamic/Exploratory mode (arguments predefined)
@pytest.mark.dynamic
@pytest.mark.relevance
@pytest.mark.sk
def test_dynamic_predefined():
    eval_type = "relevance"
    langs = ["sk"]
    generated = generate_test_input(eval_type, 5)  # Ragas + Manually written / general purpose LLM 
    translated = translate(generated, langs)       # Azure AI translator / DeepL API / Google Cloud Translation API
    output = evaluate_relevance(translated)        # Azure AI evaluation SDK / Ragas 
    publish_report(output)                         # Azure Workbooks / Power BI / Tableu


# Static mode
@pytest.mark.static
@pytest.mark.groundedness
@pytest.mark.cz
def test_static_cz():
    path_to_input = "../test_data/groundedness/cz.json"
    input = read(path_to_input)
    output = evaluate_groundedness(input)
    publish_report(output)