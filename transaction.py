# This programme contains tools for generating raw transactions and extracting transaction field data
import bitsv
import libsecp256k1
import x509_builder
import json
import requests as req
import sys
import hashlib
import binascii



def retrieve_tx(txid):
    if type(txid) != str or len(txid) > 64:
        raise Exception("input txid not formatted correctly!. txid must be a string of length 64.")
    # Gets transaction data from WhatsOnChain
    request_url = req.get("https://api.whatsonchain.com/v1/bsv/main/tx/hash/"+str(txid))
    request_json = json.loads(request_url.text)
    return request_json

def extract_certificate(txid, v_out):
    """
    Extracts OP_RETURN data and creates Python list/dict containing field values that can be accessed.
    """
    v_out = int(v_out)
    if type(txid) != str or len(txid) > 64:
        raise Exception("input txid not formatted correctly!. txid must be a string of length 64.")
    if type(v_out) != int or v_out > 2**32:
        raise Exception("input vout not formatted correctly!. txid must be a string of length 64.")
    target_tx = retrieve_tx(txid)
    target_data_list = target_tx.get('vout')[v_out]
    if sys.getsizeof(target_data_list) > tx_out_size_limit:
        raise Exception("Tx too large to parse.")

    target_opreturn = target_data_list.get('scriptPubKey').get('opReturn').get('parts')
    # Check that output is a valid OP_RETURN or OP_FALSE OP_RETURN
    if target_opreturn[0:4] == '006a':
        return json.loads(target_opreturn[1])
    elif target_opreturn[0:2] == '6a':
        return json.loads(target_opreturn[1])
    else:
        raise Exception("Not a valid data outpoint.")

def check_opreturn_prefix(opreturn):
    # Check if OP_RETURN  uses the CA prefix
    # will pass if prefix is used or not, however the certificate viewer may return an error 
    if opreturn[0] == str(x509_builder.ca_prefix) or opreturn[0] == str(x509_builder.ca_prefix) :
        return True
    else:
        print("Warning: Incorrect protocol identifier. Certificate may not be viewable.")
        return True

   

def get_pubkeys(txid):
    # Extracts the public keys used to sign validate transaction signature for txid
    target_tx_inputs = network.retrieve_tx(txid).get('vin')
    num_inputs = len(target_tx_inputs)
    key_list = dict()
    for i in range(num_inputs):
        scriptsig = target_tx_inputs[i].get('scriptSig').get('asm')
        # Must be P2PKH transaction
        key_list[i]= str(scriptsig)[len(scriptsig)-66:]
        if key_list.get(i)[0:2] != '02' and key_list.get(i)[0:2] != '03':
            raise Exception("Error: Inputs must be P2PKH.")
    return key_list

def check_pubkeys(txid):
    ca_key_list = []
    pubkeys = get_pubkeys(txid)
    # Import key list from secure file
    # Check list against hash (hard coded)
    return True









     
