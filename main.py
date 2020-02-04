import libsecp256k1
import x509_builder
import network
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
    # This is horrible, try to improve it.
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
    certificate_template = x509_builder.cert_x509().generate(subject_name, device_ID, user_ID)
    print(certificate_template)
    print("Do you wish to procceed [Y/N]?")
    input2 = input()
    if input2 == 'y' or input2 == 'Y':
        format_cert = x509builder.cert_x509().x509_format(cert_template)
        print("Certifictae (Hex):", x509builder.cert_x509().hex_encode(format_cert), "\n\n")
        print("Certifictae (Base64):", x509builder.cert_x509().base64_encode(format_cert))
    else:
        print("Terminating....")
        time.sleep(2)
        quit()


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



def main():
    print("\nWelcome to ATMackay SSL, certificate software powered by Bitcoin SV.\n\n \
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
        



