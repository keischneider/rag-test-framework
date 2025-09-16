from ragas.testset.graph import KnowledgeGraph
from ragas.testset.graph import Node, NodeType
from ragas.llms import LangchainLLMWrapper
from ragas.testset.transforms import default_transforms, apply_transforms
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from ragas.embeddings import OpenAIEmbeddings
import openai
import os
from ragas.testset import TestsetGenerator
from ragas.testset.synthesizers import default_query_distribution


generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4.1-mini"))
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
generator_embeddings = OpenAIEmbeddings(client=openai_client)


def build_kg(sections):
    kg = KnowledgeGraph()
    docs = []
    for section in sections:
        header, content = section
        doc = Document(page_content=content) #, metadata={"section_header": header}
        docs.append(doc)
        summary = "This knowledge base contains user information and sensitive data about a bank customer - John Doe."
        summary_embedding = generator_embeddings.embed_text(summary)  # pre-generate embedding for the summary
        kg.nodes.append(
            Node(
                type=NodeType.DOCUMENT,
                properties={"page_content": content, "summary": summary, "summary_embedding": summary_embedding}
            )
        )
    trans = default_transforms(documents=docs, llm=generator_llm, embedding_model=generator_embeddings)
    apply_transforms(kg, trans)
    kg_name = "knowledge_graph.json"
    kg.save(kg_name)
    return kg_name


def build_generator(kg_name):
    kg = KnowledgeGraph.load(kg_name)
    return (TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings, knowledge_graph=kg), default_query_distribution(generator_llm))
