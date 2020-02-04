# This programme contains tools for generating raw transactions and extracting transaction field data
import unittest
import libsecp256k1
import x509_builder
import network
import json


def generate_raw_tx(data, recipient, key):
    # Inputs are data payload, recipient address and signing key    
    # Generates raw transation using moneybutton API
    # Returns a JSON object 
    raw_tx = tx.json()
    return raw_tx
   

def get_pubkeys(txid):
    # Extracts the public keys used to sign validate transaction signature for txid
    target_tx_inputs = network.retrieve_tx(txid).get('vin')
    num_inputs = len(target_tx_inputs)
    key_list = dict()
    for i in range(num_inputs):
        scriptsig = target_tx_inputs[i].get('scriptSig').get('asm')
        key_list[i]= str(scriptsig)[len(scriptsig)-66:]
        if key_list.get(i)[0:2] != '02' and key_list.get(i)[0:2] != '03':
            raise Exception("Error: Inputs must be P2PKH")
    return key_list

def check_pubkeys(txid):
    ca_key_list = []
    pubkeys = get_pubkeys(txid)
    # Import key list 
    # Check list against hash (hard coded)
    return True
     
