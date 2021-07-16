#! /usr/bin/env python
import PyPDF2
import os

ENCRYPTED_FILE_PATH = '/home/vreyesr/2753445089_201101_C1.pdf'
FILE_OUT_PATH = '/home/vreyesr/output.pdf'

PASSWORD='RERV730214'

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

