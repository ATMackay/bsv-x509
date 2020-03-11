"""
Python script containing issuing private key and address.
This Python script must be encrypted while not in use.
"""
import bitsv

my_key = bitsv.Key('Kzrt4yYJFXoLmZiFivKJ3FWWX5UyXigFmhffMQUsFGXbSbggfwnL')
my_address = my_key.address
my_balance = my_key.get_balance()
my_transactions = my_key.get_transactions() # Useful for obtaining Certificate history
my_unspents = my_key.get_unspents()

