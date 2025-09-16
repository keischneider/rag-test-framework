testdata_prompt_template = """
You are a highly intelligent and detail-oriented AI assistant specializing in generating comprehensive test datasets.
Your task is to create a diverse and challenging test dataset based on the provided knowledge base, which contains detailed information about bank customers, their accounts, cards, and transactions.
The dataset should include a variety of scenarios that cover different aspects of banking operations, customer interactions, and potential edge cases.
Each test case in the dataset should be structured in JSONL format, with clear and concise fields that capture the essential elements of the scenario.
Ensure that the test cases are realistic, varied, and cover a wide range of situations that a bank customer might encounter.
The goal is to create a comprehensive dataset that can be used for evaluating the performance of large language models (LLMs) in understanding and processing complex, multi-faceted information.

Use the following context to inform your test case generation:
{context}

Characteristics of a bank customer, from the standpoint from which the questions are generated:
{persona}

Create at least {num_cases} diverse test cases, ensuring a mix of common and rare scenarios.

Possible scenarios: 
{scenarios}

The example format for each test case is as follows:
{example_format}
"""

def get_testdata_prompt_template(context, persona, scenarios, example_format, num_cases=5):
    return testdata_prompt_template.format(
        context=context, 
        persona=persona, 
        scenarios=scenarios, 
        example_format=example_format, 
        num_cases=num_cases
    )