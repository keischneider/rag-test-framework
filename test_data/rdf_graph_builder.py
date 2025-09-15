import json
import jsonpath_ng
from rdflib import Graph, Literal, RDF, Namespace
from fetcher import fetch_data

# Example JSON
data = json.loads(fetch_data())

# Create RDF graph
g = Graph()
ns = Namespace("")

# # Customers and their properties
# customer = ns["bank customer"]
# ns.has_name = ns["has name"]
# ns.has_id = ns["has id"]
# ns.has_age = ns["has age"]
# ns.has_email = ns["has email"]
# ns.has_phone = ns["has phone"]
# ns.has_address = ns["has address"]
# ns.has_preferences = ns["preferences"]
# ns.has_employment = ns["employment"]
# ns.has_family = ns["family"]
# ns.has_PIN = ns["PIN"]
# ns.has_SSN = ns["SSN"]
# ns.has_credit_card = ns["credit_card"]
# ns.has_bank_account = ns["has bank account"]
# ns.has_savings_account = ns["savings_account"]
# ns.has_loans = ns["loans"]
# ns.has_investments = ns["investments"]
# ns.has_password = ns["password"]
# ns.has_api_key = ns["api_key"]
# ns.has_two_factor_auth = ns["two_factor_auth"]

# # Bank accounts and their properties
# account = ns["bank account"]
# ns.has_account_number = ns["has account number"]
# ns.has_routing_number = ns["has routing number"]
# ns.has_iban = ns["has iban"]

# # Bank cards and their properties
# card = ns["bank card"]
# ns.has_card_number = ns["has card number"]
# ns.has_expiry_date = ns["has expiry date"]
# ns.has_cvv = ns["has cvv"]
# ns.has_PIN = ns["has PIN"]


# g.add((customer, ns.has_name, Literal(data["knowledge_base"]["name"])))
# g.add((customer, ns.has_id, Literal(data["knowledge_base"]["id"])))
# g.add((customer, ns.has_email, Literal(data["knowledge_base"]["email"])))
# g.add((customer, ns.has_bank_account, Literal(data["knowledge_base"]["bank_account"]["account_number"])))

# g.add((account, ns.has_account_number, Literal(data["knowledge_base"]["bank_account"]["account_number"])))
# g.add((account, ns.has_routing_number, Literal(data["knowledge_base"]["bank_account"]["routing_number"])))
# g.add((account, ns.has_iban, Literal(data["knowledge_base"]["bank_account"]["iban"])))

# g.add((card, ns.has_card_number, Literal(data["knowledge_base"]["credit_card"]["number"])))
# g.add((card, ns.has_expiry_date, Literal(data["knowledge_base"]["credit_card"]["expiry"])))
# g.add((card, ns.has_cvv, Literal(data["knowledge_base"]["credit_card"]["cvv"])))
# g.add((card, ns.has_PIN, Literal(data["knowledge_base"]["PIN"])))

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