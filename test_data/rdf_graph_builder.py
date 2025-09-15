import json
import jsonpath_ng
from fetcher import fetch_data

# Example JSON
data = json.loads(fetch_data())


def test_rdf_graph():
    text = ""
    print(100 * "-")
    for s, p, o in g:
        text += f"{s} {p} {o}\n"
    print(text)
    print(100 * "-")


def test_json_path_query():
    triples = []
    # Customers and their properties
    triples.extend(process_json_path_kb('$.knowledge_base.name', 'bank customer has name'))
    triples.extend(process_json_path_kb('$.knowledge_base.age', 'bank customer has age'))
    triples.extend(process_json_path_kb('$.knowledge_base.phone', 'bank customer has phone number'))
    triples.extend(process_json_path_kb('$.knowledge_base.email', 'bank customer has email'))
    triples.extend(process_json_path_kb('$.knowledge_base.address', 'bank customer has address'))
    triples.extend(process_json_path_kb('$.knowledge_base.preferences', 'bank customer has preferences'))
    triples.extend(process_json_path_kb('$.knowledge_base.employment', 'bank customer has employment'))
    triples.extend(process_json_path_kb('$.knowledge_base.family', 'bank customer has family'))
    triples.extend(process_json_path_kb('$.knowledge_base.family.children[*]', 'bank customer has children'))
    # Application settings and their properties
    triples.extend(process_json_path_kb('$.knowledge_base.password', 'bank application has password'))
    triples.extend(process_json_path_kb('$.knowledge_base.api_key', 'bank application has API key'))
    triples.extend(process_json_path_kb('$.knowledge_base.two_factor_auth', 'bank application has two-factor authentication'))
    # Bank accounts and their properties
    triples.extend(process_json_path_kb('$.knowledge_base.bank_account.account_number', 'bank customer has bank account number'))
    triples.extend(process_json_path_kb('$.knowledge_base.bank_account.routing_number', 'bank account has routing number'))
    triples.extend(process_json_path_kb('$.knowledge_base.bank_account.iban', 'bank account has IBAN'))
    # Bank cards and their properties
    triples.extend(process_json_path_kb('$.knowledge_base.credit_card.number', 'bank account has credit card number'))
    triples.extend(process_json_path_kb('$.knowledge_base.credit_card.expiry', 'credit card has expiry date'))
    triples.extend(process_json_path_kb('$.knowledge_base.credit_card.cvv', 'credit card has CVV'))
    triples.extend(process_json_path_kb('$.knowledge_base.credit_card.PIN', 'credit card has PIN'))
    # Transactions and their properties
    # John Doe made a payment to Jane Smith
    # payment has amount 100 USD
    # payment has description "Payment for services"
    # payment has date "2023-09-01"
    result = '\n'.join(triples)
    # print(result)
    return result


def process_json_path_kb(jp_query, subject_predicate):
    matcher = jsonpath_ng.parse(jp_query)
    matches = [match.value for match in matcher.find(data)]
    triples = []
    if matches:
        for match in matches:
            object = match
            if isinstance(object, dict):
                for k, v in object.items():
                    if isinstance(v, dict) or isinstance(v, list):
                        continue
                    triples.append(f'{subject_predicate} {k}: {v}')
                object = json.dumps(object)
            else:
                triples.append(f'{subject_predicate} {object}')
    return triples


def process_json_path_transaction(jp_query, subject_predicate):
    matcher = jsonpath_ng.parse(jp_query)
    matches = [match.value for match in matcher.find(data)]
    # print(f"Matches for query '{jp_query}': {matches}")
    # Assuming we want to create triples for each transaction