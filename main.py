import libsecp256k1
import x509_builder


def main():
    print("Enter Subject name:")
    subject_name = input()
    print("Enter Subject company:")
    subject_company = input()
    print("Enter Subject device type:")
    device_type = input()
    device_ID = x509_builder.gen_device_id(subject_name, device_type)
    user_ID = x509_builder.user_id(subject_name, subject_company)
    print("Enter Issuer Username:")
    issuer = input()
    print("Enter Password:")
    pass_attempt = input()
    libsecp256k1.password_check(pass_attempt)
    # View certificate
    certificate_template = x509builder.cert_x509().generate(subject_name, device_ID, user_ID)
    print(certificate_template)
    print("Do you wish to procceed [Y/N]?")
    input2 = input()
    if input2 == 'y' or input2 == 'Y':
        format_cert = x509builder.cert_x509().x509_format(certificate_template)
        print("Certifictae (Hex):", x509builder.cert_x509().hex_encode(format_cert), "\n\n")
        print("Certifictae (Base64):", x509builder.cert_x509().base64_encode(format_cert))

if __name__=="__main__":       
    main()
        
    


# Prompt: Enter certified entity name 

# generate key pair? Y/N

# Enter issuer name: enter string up to 20 characters

# View certificate:

# Do you wish to sign and proceed?

# Enter Issuer key: private key 

# Are you sure: 

# complete certificate, hex and Base64, encoded:


