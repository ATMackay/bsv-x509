# Test pieces of the code
import libsecp256k1 
import unittest
import x509_builder
import network
import transaction
import json

# Exracts OP_RETURN data from example transaction (txid below)


example_txid = '28487c32c7fe6e73467c07e903f25bdead33e439591e603b23bfeaf7ee5570be'

target_tx = transaction.retrieve_tx(example_txid)
target_data_list = target_tx.get('vout')[0]
target_opreturn = target_data_list.get('scriptPubKey').get('opReturn').get('parts')
target_opreturn_hex = target_data_list.get('scriptPubKey').get('hex')

print("\n\n", target_tx)
print("\n\n", target_opreturn)
print("\n\n", target_opreturn_hex)

opreturn_json = json.loads(target_opreturn[1])

print("\n\n", opreturn_json["Subject public key"])


