import libsecp256k1
import x509_builder
import network 
import transaction
import test
import time
import sys
from getpass import getpass



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
    i = 0
    while i < 4:
        pass_attempt = getpass()
        if libsecp256k1.password_check(pass_attempt) != True:
            if i > 2:
                print("\nPassowrd authentication failed. Aborting....")  
                quit()            
            print("\nPassowrd attempt failed. You have "+str(3-i)+" remaining attempts.")
            i += 1
        else:
            break
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
        print("\n\nCertifictae (Hex):", transaction.generate_opreturn(certificate_data))
    else:
        print("Terminating....")
        time.sleep(2)
        quit()
    print("Do you wish to sign with Issuing key? [Y/N]")
    input3 = input()
    if input3 == 'y' or input3 == 'Y':
        print(network.retrieve_tx(test.tx_id))
    else:
        print("Terminating....")
        time.sleep(2)
        quit()
    print("\n Warning: The data to publish to the Bitcoin SV blockcahin will remain there forever.")
    pass_attempt2 = getpass()
    print("\n\nBroadcasting to the Bitcoin SV network...")
    time.sleep(2)
    print("\n\nTransaction ID:"+str(test.tx_id))
    #print("\n\nTransaction ID:"+str(TRANSACTION ID))


def validate_certificate():
    print("Enter certificate TXID")
    cert_txid = input()
    print("Enter certificate VOUT")
    cert_vout = input()
    # Get certificate
    cert_tx = network.retrieve_tx(cert_txid)
    print(cert_tx)
    print("Extracting OP_RETURN...")
    time.sleep(2)
    cert_data = network.extract_nulldata(cert_txid)
    certificate = x509_builder.decode(cert_data)
    formatted_cert = x509_builder.json_format(certificate)
    print(certificate)
    print("\n\nValidating chain of trust")
    time.sleep(1)
    # Get public keys --> print(transaction.get_pubkeys(txid))
    # Print public keys 
    # Validate public keys 
    print("\n\nExtracting intermediate certificate.")
    intermed_txid = cert_data[3]
    intermed_vout = cert_data[4]
    # Print intermediate certificate 
    # Get public keys --> print(transaction.get_pubkeys(cert_data[3]))
    time.sleep(1)
    print("\n\nExtracting root certificate.")
    root_txid = cert_data[5]
    root_vout = cert_data[6]
    # Print root certificate
    # Get public keys --> print(transaction.get_pubkeys(cert_data[5]))
    #if keys valid then authentication success else fail 





def main():
    print("\nWelcome to CT-AM SSL, certificate software powered by Bitcoin SV.\n\n \
        Press (1) to create a new certificate, or \n         press (2) to validate an on chain certificate.\n \
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
        



