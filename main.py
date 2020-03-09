import keys
import libsecp256k1
import x509_builder
import network 
import transaction
import test
import time
import sys
import json
from getpass import getpass

# Alex edit 06-03-2020

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
    #libsecp256k1.passwd()
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
        payload =  [x509_builder.ca_prefix.encode('utf-8'), format_cert.encode('utf-8')]#!!!!!!!!!!!!!!!!!!!!! FIX
        print("\n\nCertificate (Hex):", payload)
    else:
        print("Terminating....")
        time.sleep(2)
    print("Do you wish to sign with issuing key? [Y/N]")
    input3 = input()
    if input3 == 'y' or input3 == 'Y':
        # Decrypt_wallet
        # Extract issuing key
        # Create transaction paying from and to issuing key containing OP_RETURN
        my_key = keys.my_key #Insecure
        print(keys.my_unspents)
        print(keys.my_transactions)
        raw_tx = my_key.create_op_return_tx(payload)
        print(raw_tx)
        # This need to be re-written
    else:
        print("Terminating....")
        time.sleep(2)
    print("\nWarning: The data you publish to the Bitcoin SV blockchain is immutable. Once broadcast it will remain there forever.")
    libsecp256k1.passwd()
    print("\n\nBroadcasting to the Bitcoin SV network...")
    # network.braodcast(raw_tx) --> get response TRANSACTION ID
    # Check that network has seen transaction 
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
                print("Transaction unconfirmed after "+str(limit)" attempts, aborting...")
                print("\nManually check for transaction on https://www.whatsonchain.com")
                print("\nTransaction ID: ", txid)
                
            else:
                print("Transaction unconfirmed, retrying in 5 seconds...")
                time.sleep(5)
                tx_list = my_key.get_transactions()
        else:
            print("Transaction confirmed...")
            break
        

# e1f250f0d1f95bc6a9874216604bb19b8805343b55752616647d4df11c8f710d

def validate_certificate():
    print("Enter certificate TXID")
    cert_txid = input()
    print("Enter certificate VOUT")
    cert_vout = input()
    # Get certificate
    cert_tx = network.retrieve_tx(cert_txid)
    print(cert_tx)
    print("\n\nExtracting OP_RETURN...")
    time.sleep(2)
    #Dummy for PoC
    cert_data = network.extract_nulldata(cert_txid, cert_vout)
    certificate_bytes = transaction.decode_opreturn(cert_data)
    print("\n", certificate_bytes)
    # Need to convert OP_RETURN data to string
    # Still need to clear up the encoding and decoding path
    print("\n\nValidating chain of trust")
    time.sleep(1)
    # Get public keys
    print("\n\nValidating issuer key...") 
    print(transaction.get_pubkeys(cert_txid))
    time.sleep(1)
    print("Issuer certificate is valid.")
    # Validate public keys 
    print("\n\nExtracting intermediate certificate...")
    intermed_txid = test.ex1_int_txid  #cert_data[3]
    #intermed_vout = cert_data[4]
    # Print intermediate certificate 
    print("\n\nValidating policy key...") 
    print(transaction.get_pubkeys(intermed_txid))
    time.sleep(1)
    print("Policy certificate is valid.")
    # Get public keys --> print(transaction.get_pubkeys(cert_data[3]))
    time.sleep(1)
    print("\n\nExtracting root certificate...")
    root_txid = test.ex2_root_txid  #cert_data[5]
    #root_vout = cert_data[6]
    print("\n\nValidating root key...") 
    print(transaction.get_pubkeys(root_txid))
    time.sleep(1)
    print("Root certificate is valid.")
    time.sleep(1)
    print("\n\nAuthentication successful.")
    #if keys valid then authentication success else fail 





def main():
    print("\nWelcome to CT-AM SSL, certificate software powered by Bitcoin SV.\n\n \
            Please Enter Password:")
    #libsecp256k1.passwd()
    print("\nPress (1) to create a new certificate, or \n         press (2) to validate a BSV SSL certificate.\n \
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

if __name__=="__main__":       
    main()
        



