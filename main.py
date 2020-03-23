import keys
import root_data
import libsecp256k1
import x509_builder
import network 
import transaction
import time
import sys
import json
from getpass import getpass



def create_certificate():
    print("Creating a Bitcoin SV SSL certificate..")
    time.sleep(1)
    print("\nEnter Subject name:")
    subject_name = input()
    sub_key = keys.my_address #Example. change to input user key
    print("\nSubject Public Key:", sub_key)
    print("\nEnter Subject company:")
    subject_company = input()
    print("\nEnter Subject device type:")
    device_type = input()
    libsecp256k1.passwd()
    # Instantiate certificate class
    certificate = x509_builder.cert(subject_name, subject_company, device_type, sub_key)
    certificate_template = certificate.generate()
    format_cert = certificate.json_format(certificate_template)
    print("######################## CERTIFICATE ######################")
    print(format_cert)
    print("Do you wish to procceed [Y/N]?")
    input2 = input()
    time.sleep(1)
    if input2 == 'y' or input2 == 'Y':
        # Needs to be a JSON string
        payload =  [x509_builder.ca_prefix.encode('utf-8'), format_cert.encode('utf-8')]
        print("\n\nCertificate Payload:", payload)
    else:
        print("Terminating....")
        time.sleep(2)
    print("Do you wish to sign with issuing key? [Y/N]")
    input3 = input()
    if input3 == 'y' or input3 == 'Y':
        # Create transaction paying from and to issuing key containing OP_RETURN
        my_key = keys.my_key #Insecure
        raw_tx_bytes = my_key.create_op_return_tx(payload)
        print("Payload bytes:", raw_tx_bytes)
        # This need to be re-written
    else:
        print("Terminating....")
        time.sleep(2)
    print("\nWarning: The data you publish to the Bitcoin SV blockchain is immutable. Once broadcast it will remain there forever.")
    libsecp256k1.passwd()
    print("\n\nBroadcasting to the Bitcoin SV network...")
    # network.broadcast(raw_tx) --> get response TRANSACTION ID
    # Check that the network has seen the transaction 
    txid = my_key.send_op_return(payload)
    time.sleep(1)
    print("\n\nTransaction ID:" + str(txid))
    time.sleep(2)
    print("\n\nChecking WhatsonChain...")
    time.sleep(5)
    tx_list = my_key.get_transactions()
    limit = 5
    for i in range(limit):
        if txid  not in tx_list:
            if i >= limit - 1:
                print("Transaction unconfirmed after "+str(limit)+" attempts, aborting...")
                print("\nManually check for transaction on https://www.whatsonchain.com")
                print("\nTransaction ID: ", txid)
                
            else:
                print("Transaction unconfirmed, retrying in 5 seconds...")
                time.sleep(5)
                tx_list = my_key.get_transactions()
        else:
            print("Transaction confirmed...")
            break
        

def validate_certificate():
    print("Enter certificate TXID")
    cert_txid = input()
    print("Enter certificate VOUT")
    cert_vout = input()
    # Get certificate
    cert_tx = transaction.retrieve_tx(cert_txid)
    print(cert_tx)
    print("\n\nExtracting OP_RETURN...")
    time.sleep(2)
    cert_data = transaction.extract_certificate(cert_txid, cert_vout)
    print("\n", cert_data)
    time.sleep(1)    
    print("\nCertified Key: ", cert_data["Subject public key"])
    print("\n\nValidating chain of trust..")
    time.sleep(1)
    # Get public keys
    print("\n\nValidating issuer key...") 
    sign_keys = transaction.get_pubkeys(cert_txid)
    print("Signing Key:", sign_keys[0])
    if root_data.root_data["intermediate key"] not in sign_keys.values():
        print("\n Invalid issuing key... aborting.")
        time.sleep(1)
        quit()
    else:
        time.sleep(1)
        print("Issuer certificate is valid.")
    # Validate public keys 
    print("\n\nExtracting intermediate certificate...")
    intermed_txid = cert_data["Intermediate certificate txid"] 
    inter_keys = transaction.get_pubkeys(intermed_txid)
    print("Intermediate certificate TXID: ", intermed_txid)
    print("Policy Key: ", inter_keys[0])
    if root_data.root_data["root key"] not in inter_keys.values():
        print("\n Invalid policy key... aborting.")
        time.sleep(1)
        quit()
    else:
        time.sleep(1)
        print("Policy certificate is valid.")
    time.sleep(1)
    print("\n\nExtracting root certificate...")
    root_txid = cert_data["Root certificate txid"] 
    root_keys = transaction.get_pubkeys(root_txid)
    print("Root certificate TXID: ", root_txid)
    print("Root key: ", root_keys[0])
    # Self-signed root key
    if root_data.root_data["root key"] not in root_keys.values():
        print("\n Invalid root key... aborting.")
        time.sleep(1)
        quit()
    else:
        time.sleep(1)
        print("Root certificate is valid.")
    time.sleep(1)
    print("\n\n Authentication successful.")
    #if keys valid then authentication success else fail 


def main():
    print("\nCT-AM SSL, certificate software powered by Bitcoin SV.\n\n \
            Please Enter Password:")
    libsecp256k1.passwd()
    print("\nPress (1) to create a new certificate, or \nPress (2) to validate a BSV SSL certificate.\n \
            Press any other key to exit.")
    value1 = input()
    if value1 == '1':
        create_certificate()
    elif value1 == '2':
        validate_certificate()
    else: 
        print("Exiting...")
        time.sleep(2)
        quit()

if __name__ == "__main__":       
    main()
        



