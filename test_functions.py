import bitsv
import libsecp256k1
#import x509_builder
#import network 
#import transaction
import time
import sys
import json
from getpass import getpass


my_key = bitsv.Key('Kzrt4yYJFXoLmZiFivKJ3FWWX5UyXigFmhffMQUsFGXbSbggfwnL')
my_address = my_key.address
my_balance = my_key.get_balance()
my_transactions = my_key.get_transactions() # Useful for obtaining Certificate history
my_unspents = my_key.get_unspents()
my_balance_usd = my_key.balance_as('usd')

#new_key = bitsv.generate_key_address_pair()

print("Balance:", my_balance)
print("My address", my_address)
print("Balance USD:", my_balance_usd)
print("Key:", my_key)
print("My TXIDs:", my_transactions)
print("My UTXOS:", my_unspents)


# Test transaction generation
fee = 250
bal = int(my_balance)
am = bal - fee

#am = am/10e8
print(am)

list_of_pushdata =  ['JSON string'.encode('utf-8')]
tx_data = my_key.prepare_transaction(my_address, [("18aM1rxZL5wCmTrL9MVPjN7NAWjEM2jeHV", am, 'satoshi')], list_of_pushdata)
print("transaction:", tx_data)

signed_tx = my_key.sign_transaction(tx_data)
print("\n\nSigned Tx:", signed_tx)



tx_opreturn = my_key.create_op_return_tx(list_of_pushdata) #!!!!! this is what you need, simple 1 in 2 out with op_return
print("\n", tx_opreturn)


"""
my_key = bitsv.Key('Kzrt4yYJFXoLmZiFivKJ3FWWX5UyXigFmhffMQUsFGXbSbggfwnL')
my_address = my_key.address
my_balance = my_key.get_balance()
my_balance = my_key.balance_as('bsv')
my_transactions = my_key.get_transactions() # Useful for obtaining Certificate history
my_unspents = my_key.get_unspents()
my_balance_usd = my_key.balance_as('usd')

#new_key = bitsv.generate_key_address_pair()

print("Balance:", my_balance)
print("My address", my_address)
print("Balance USD:", my_balance_usd)
print("Key:", my_key)
print("My TXIDs:", my_transactions)
print("My UTXOS:", my_unspents)


# Test transaction generation
fee = 0.00000250
am = float(my_balance) - fee

#am = am/10e8
print(am)
tx_data = my_key.prepare_transaction(my_address, [("18aM1rxZL5wCmTrL9MVPjN7NAWjEM2jeHV", 0.00004, 'jpy')])
print(tx_data)

signed_tx = my_key.sign_transaction(tx_data)
print(signed_tx)
"""
