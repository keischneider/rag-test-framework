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


# Plan 🧭
# create your fist custom evaluator for relevancy
# use ragas evaluator
# compare the results with your custom evaluator
# 1. Embedding based relevancy evaluator
    # To check relevancy, we can use cosine similarity between embeddings of the question and the answer.
    # We can use OpenAI's embedding model to generate embeddings for both the question and the answer.
    # Then, we can calculate the cosine similarity between the two embeddings.
    # If the cosine similarity is above a certain threshold, we can consider the answer to be relevant to the question.
    # We can use the following steps to implement this:
    # 1. Generate embeddings for the question and the answer using OpenAI's embedding model
    # 2. Calculate the cosine similarity between the two embeddings
# 2. LLM-as-a-judge evaluator
    # We can use a language model to evaluate the relevancy of the answer to the question
    # by prompting the model with the question and the answer and asking it to rate the relevancy on a scale of 1 to 10.
    # We can use the following steps to implement this:
    # 1. Create a prompt that includes the question and the answer
    # 2. Use the language model to generate a response to the prompt
    # 3. Parse the response to extract the relevancy rating

# Sources 📚
# Microsoft
# https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-evaluation_1.0.0b5/sdk/evaluation/azure-ai-evaluation
# https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-evaluation_1.0.0b5/sdk/evaluation/azure-ai-evaluation/azure/ai/evaluation/_evaluators/_relevance/relevance.prompty
# Azure AI search tailored relevance evaluator - https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/Supported_Evaluation_Metrics/RAG_Evaluation/Optimize_RAG_with_Document_Retrieval_Evaluator.ipynb

# Ragas
# https://docs.ragas.io/en/stable/getstarted/rag_eval/#load-documents

# create your fist custom evaluator for groundedness
# 1. Entity-based groundedness evaluator
    # To check groundedness, we can extract entities from the answer and check if they are present in the context.
    # We can use a named entity recognition (NER) model to extract entities from the answer.
    # Then, we can check if the extracted entities are present in the context.
    # If a certain percentage of the extracted entities are present in the context, we can consider the answer to be grounded.
    # We can use the following steps to implement this:
    # 1. Use a NER model to extract entities from the answer
    # 2. Check if the extracted entities are present in the context
# 2. LLM-as-a-judge evaluator
    # We can use a language model to evaluate the groundedness of the answer by prompting the model with the context and the answer
    # and asking it to rate the groundedness on a scale of 1 to 10.
    # We can use the following steps to implement this:
    # 1. Create a prompt that includes the context and the answer
    # 2. Use the language model to generate a response to the prompt
    # 3. Parse the response to extract the groundedness rating

# think of a usual pipeline from test data generation to evaluation


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