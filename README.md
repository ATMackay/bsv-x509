# bsv-x509
This program generates/validates x.509 public key certificates and publishes them to the Bitcoin SV blockchain.
To run you will need to have installed the following

* Python 3.6 or later

Running bsv-x509

Linux:

    1) Go the the bsv-x509 directory

        ~/$PATH/bsv-x509

    2)  Verify SHA512 fingerprint of the root data file
        
        ~/$PATH/bsv-x509 sha512sum root_data.py

        The return value should equal --> 7726cad0b4aa63d285cf6038d7220e10ba5d7f1737c4ffbf0d2bda79e44d6e5df822d818892fed8aa91bb412919eeedb04739cff1f8d58a65e5a7f7e06edc2bc  root_data.py

        If the fingerprint values do not match DO NOT EXECUTE the main program

    3)  To execute the certificate viewer run the main.py file 

        ~/$PATH/bsv-x509 python3 main.py

    3) Follow instructions to create or validate digital certificates on the BSV blockchain

Example Transactions (WhatsOnChain.com)

* https://whatsonchain.com/tx/09bf2e97d4bccf6f76fec796b1062af496c23414b146a75a018cc40990964400
* https://whatsonchain.com/tx/5aa85ef98aa2514967ad039a6675e55c8f0b367f68dd27da859e1449a1657bd1

© 2019 nChain Limited. All rights reserved. This software is provided without any warranties whatsoever and shall not result in the grant of any license, whether implied or otherwise. nChain Limited shall not be liable in any way for the use of the information provided herein.
