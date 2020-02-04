# Test pieces of the code 
import unittest
import libsecp256k1
import x509_builder
import network
import transaction




# Unit Test
tx_id = "81d29f7cd268249d33e617e511221718ac2b955a1b3f0a3b915e122bd904bb3e"
tx_id2 = "5f40fa5a4291b369035cb65d2a0086c3e3b05f7e95efca0682a418f6929dec0b"
print(network.retrieve_tx(tx_id), "\n \n")
print(transaction.get_pubkeys(tx_id))
#print(extract_nulldata(tx_id2, 0), "\n \n")

