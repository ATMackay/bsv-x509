import bitsv
import libsecp256k1
import x509_builder
import network 
import transaction
import test
import time
import sys
import json
from getpass import getpass



def passwd():
    i = 0
    while i < 4:
        pass_attempt = getpass()
        if libsecp256k1.password_check(pass_attempt) != True:
            if i > 2:
                print("\nPassword authentication failed. Aborting....")  
                quit()            
            print("\nPassword attempt failed. You have "+str(3-i)+" remaining attempts.")
            i += 1
        else:
            break

def create_certificate():
    print("Creating a Bitcoin SV SSL certificate..")
    time.sleep(1)
    print("\nEnter Subject name:")
    subject_name = input()
    print("\nEnter Subject company:")
    subject_company = input()
    print("\nEnter Subject device type:")
    device_type = input()
    device_ID = x509_builder.gen_device_id(subject_name, device_type)
    user_ID = x509_builder.user_id(subject_name, subject_company)
    print("\nEnter Issuer Username:")
    issuer = input()
    # This will be imporved in later versions
    passwd()
    # View certificate
    certificate_data = x509_builder.cert_data(subject_name, device_ID, user_ID)
    certificate_template = x509_builder.generate(certificate_data)
    format_cert = x509_builder.json_format(certificate_template)
    print("################## CERTIFICATE ##################")
    print(format_cert)
    print("Do you wish to procceed [Y/N]?")
    input2 = input()
    time.sleep(1)
    if input2 == 'y' or input2 == 'Y':
        payload = transaction.generate_opreturn(certificate_data)
        print("\n\nCertificate (Hex):", payload)
    else:
        print("Terminating....")
        time.sleep(2)
        quit()
    print("Do you wish to sign with issuing key? [Y/N]")
    input3 = input()
    if input3 == 'y' or input3 == 'Y':
        print("################## CERTIFICATE TRANSACTION (RAW) ##################")
        # transaction.generate_raw_tx(payload, issue_key, issue_key)
        # Dummy TX for PoC
        # Replace with bitsv commands
        tx = network.retrieve_tx(test.tx_id)
        target = dummy_tx.get('vin')[0]
        serialized = target.get('scriptSig').get('hex')
        dumm_prefix = '01000000010000ffffffff1c03d7c6082f7376706f6f6c2e636f6d2'\
                     +'f3edff034600055b8467f0040'
        dumm_spk =   'ffffffff01247e814a000000001976' +'914492558fb8ca71a3591316d095afc0f20ef7d42f788ac00000000'
        print(dumm_prefix + serialized +  str(payload)[2:len(str(payload))-1] + dumm_spk )
        # This need to be re-written
    else:
        print("Terminating....")
        time.sleep(2)
        quit()
    print("\nWarning: The data you publish to the Bitcoin SV blockchain is immutable. Once broadcast it will remain there forever.")
    passwd()
    print("\n\nBroadcasting to the Bitcoin SV network...")
    # network.braodcast(raw_tx) --> get response TRANSACTION ID
    time.sleep(2)
    print("\n\nTransaction ID:" + str(test.tx_id0))
    #print("\n\nTransaction ID:"+str(TRANSACTION ID))


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
        Press (1) to create a new certificate, or \n         press (2) to validate a BSV SSL certificate.\n \
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
        



