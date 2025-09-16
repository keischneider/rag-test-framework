import json
import jsonpath_ng


def convert_to_triples_from(json_data):
    triples = []
    jp_triple_pairs = [
        # Transactions and their properties
        ('$.knowledge_base.name', 'bank customer has name'),
        ('$.knowledge_base.age', 'bank customer has age'),
        ('$.knowledge_base.phone', 'bank customer has phone number'),
        ('$.knowledge_base.email', 'bank customer has email'),
        ('$.knowledge_base.address', 'bank customer has address'),
        ('$.knowledge_base.preferences', 'bank customer has preferences'),
        ('$.knowledge_base.employment', 'bank customer has employment'),
        ('$.knowledge_base.family', 'bank customer has family'),
        ('$.knowledge_base.family.children[*]', 'bank customer has children'),
        # Application settings and their properties
        ('$.knowledge_base.password', 'bank application has password'),
        ('$.knowledge_base.api_key', 'bank application has API key'),
        ('$.knowledge_base.two_factor_auth', 'bank application has two-factor authentication'),
        # Bank accounts and their properties
        ('$.knowledge_base.bank_account.account_number', 'bank customer has bank account number'),
        ('$.knowledge_base.bank_account.routing_number', 'bank account has routing number'),
        ('$.knowledge_base.bank_account.iban', 'bank account has IBAN'),
        # Bank cards and their properties
        ('$.knowledge_base.credit_card.number', 'bank account has credit card number'),
        ('$.knowledge_base.credit_card.expiry', 'credit card has expiry date'),
        ('$.knowledge_base.credit_card.cvv', 'credit card has CVV'),
        ('$.knowledge_base.credit_card.PIN', 'credit card has PIN')
    ]
    for jp_query, subject_predicate in jp_triple_pairs:
        triples.extend(convert_json_entry_to_triples(json_data, jp_query, subject_predicate))

    # Transactions and their properties
    matcher = jsonpath_ng.parse('$.transactions[*]')
    matches = [match.value for match in matcher.find(json_data)]
    for match in matches:
        triples.append(f'{match['sender']} made payment to {match['recipient']}')
        triples.append(f'payment has amount of {match['amount']} {match['currency']}')
        triples.append(f'payment has description {match['description']}')
        triples.append(f'payment has date {match['datetime']}')
    result = '\n'.join(triples)
    return result


def convert_json_entry_to_triples(data, jp_query, subject_predicate):
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