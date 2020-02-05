# This programme connects to Bitcoin SV endpoints for broadcasting/retrieving transaction 
# blockchain data. This programme depends on WhatsOnChain.com servers for data
import libsecp256k1
import transaction
import json
import requests as req
import sys



tx_out_size_limit = 100000

def retrieve_tx(txid):
    if type(txid) != str or len(txid) > 64:
        raise Exception("input txid not formatted correctly!. txid must be a string of length 64.")
    # Gets transaction data from WhatsOnChain
    request_url = req.get("https://api.whatsonchain.com/v1/bsv/main/tx/hash/"+str(txid))
    request_json = json.loads(request_url.text)
    return request_json

def extract_nulldata(txid, v_out):
    if type(txid) != str or len(txid) > 64:
        raise Exception("input txid not formatted correctly!. txid must be a string of length 64.")
    if type(v_out) != int or v_out > 2**32:
        raise Exception("input txid not formatted correctly!. txid must be a string of length 64.")
    target_tx = retrieve_tx(txid)
    target_data_list = target_tx.get('vout')[v_out]
    if sys.getsizeof(target_data_list) > tx_out_size_limit:
        raise Exception("Tx too large to parse.")

    target_opreturn = target_data_list.get('scriptPubKey').get('hex')
    # Check that output is a valid OP_RETURN or OP_FALSE OP_RETURN
    if target_opreturn[0:4] != '006a':
        raise Exception("Not a valid data outpoint")
    return target_opreturn[4:]


def broadcast(raw_tx):
    # raw_tx must be a JSON object
    request_post = req.post("https://api.whatsonchain.com/v1/bsv/main/tx/raw/", my_tx)
    return raw_tx

