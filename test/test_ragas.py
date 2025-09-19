import pytest
import json
from test_data.utils import fetch_data
from langchain_openai import ChatOpenAI
from ragas.embeddings import OpenAIEmbeddings
import openai
from ragas import EvaluationDataset
from ragas.llms import LangchainLLMWrapper
from ragas import evaluate
from ragas.metrics import ResponseRelevancy, ContextRecall


llm = ChatOpenAI(model="gpt-4.1-mini")
openai_client = openai.OpenAI()
embeddings = OpenAIEmbeddings(client=openai_client)
evaluator_llm = LangchainLLMWrapper(llm)


@pytest.mark.ragas_relevance
def test_example():
    # try to run same evaluation via jupiter notebook
    dataset = []
    test_data = fetch_data('../test_data/test_questions/344342342.jsonl').splitlines()
    for line in test_data:
        line = json.loads(line)
        dataset.append({
            "user_input": line["input"],
            "response": line["output"]
        })
    evaluation_dataset = EvaluationDataset.from_list(dataset)
    result = evaluate(dataset=evaluation_dataset,metrics=[ResponseRelevancy()],llm=evaluator_llm)
    print(result)
    print(result.to_pandas())


@pytest.mark.ragas_groundedness
def test_example_groundedness():
    # try to run same evaluation via jupiter notebook
    dataset = []
    test_data = fetch_data('../test_data/test_questions/1758040490.jsonl').splitlines()
    for line in test_data:
        line = json.loads(line)
        dataset.append({
            "user_input": line["input"],
            "retrieved_contexts": [line["reference_context"]],
            "reference": line["output"]
        })
    evaluation_dataset = EvaluationDataset.from_list(dataset)
    result = evaluate(dataset=evaluation_dataset,metrics=[ContextRecall()],llm=evaluator_llm)
    print(result)
    result.to_pandas().to_csv('groundedness_results.csv')
    print(result.to_pandas())