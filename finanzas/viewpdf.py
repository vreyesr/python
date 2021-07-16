#! /usr/bin/env python
import PyPDF2
import os

ENCRYPTED_FILE_PATH = './files/executive_order_encrypted.pdf'
FILE_OUT_PATH = './files/executive_order_out.pdf'

PASSWORD='hoge1234'

with open(ENCRYPTED_FILE_PATH, mode='rb') as f:
    reader = PyPDF2.PdfFileReader(f)
    if reader.isEncrypted:
        try:
            reader.decrypt(PASSWORD)
        except NotImplementedError:
            command=f"qpdf --password='{PASSWORD}' --decrypt {ENCRYPTED_FILE_PATH} {FILE_OUT_PATH};"
            os.system(command)
            with open(FILE_OUT_PATH, mode='rb') as fp:
                reader = PyPDF2.PdfFileReader(fp)
                print(f"Number of page: {reader.getNumPages()}")

import PyPDF2

# creating a pdf file object



ENCRYPTED_FILE_PATH = 'D:\\vbrr_data\\finanazas\\ahorro\\bancomer\\5089\\2011\\2753445089_201101_C1.pdf'

with open(ENCRYPTED_FILE_PATH, mode='rb') as f:
    reader = PyPDF2.PdfFileReader(f)
    if reader.isEncrypted:
        reader.decrypt('RERV730214')
        print(f"Number of page: {reader.getNumPages()}")