# This programme connects to Bitcoin SV endpoints for broadcasting/retrieving transaction 
# blockchain data. This programme depends on WhatsOnChain.com servers for data
import libsecp256k1
import transaction
import json
import requests as req
import sys


def broadcast(raw_tx):
    # raw_tx must be a JSON object
    request_post = req.post("https://api.whatsonchain.com/v1/bsv/main/tx/raw/", my_tx)
    return raw_tx

