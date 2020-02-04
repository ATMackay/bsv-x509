# This programme connects to Bitcoin SV endpoints for broadcasting/retrieving transaction 
# blockchain data. This programme depends on WhatsOnChain.com servers for data

import json
import requests as req
import sys
import libsecp256k1


def retrieve_tx(txid):
    if type(txid) != str or len(txid) > 64:
        raise Exception("input txid not formatted correctly!. txid must be a string of length 64.")
    request_url = req.get("https://api.whatsonchain.com/v1/bsv/main/tx/hash/"+str(txid))
    rq_format = str(request_url.content)[1:]
    request_json = json.dumps(rq_format)
    return request_json

def extract_nulldata(txid):
    if type(txid) != str or len(txid) > 64:
        raise Exception("input txid not formatted correctly!. txid must be a string of length 64.")
    target_tx = retrieve_tx(txid)
    target_data = target_tx.get("opReturn")
    if target_data == "null":
        raise Exception("No OP_RETURN data.")
    return target_data

def get_pubkey():
    target_tx = json.load(retrieve_tx(txid))
    target_scriptpubkey = target_tx.get("scriptSig")
       

def broadcast(raw_tx):
    return raw_tx

# Unit Test
tx_id = "81d29f7cd268249d33e617e511221718ac2b955a1b3f0a3b915e122bd904bb3e"
print(retrieve_tx(tx_id))
print(extract_nulldata(tx_id))
