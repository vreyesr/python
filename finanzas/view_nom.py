#! /usr/bin/python3

from lxml import etree
import os
import fnmatch
import sys
import argparse
from tabulate import tabulate



def parse_args():
    parser = argparse.ArgumentParser(prog="facturas.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Database reports for LibreNMS and SWR")

    parser.add_argument('-f', '--filename', dest="filename", help="Specific a XML file")
    local_args = parser.parse_args()

    try:
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
    except Exception:
        sys.exit(1)

    return local_args


def viewnom(file_name):
    root = etree.parse(file_name).getroot()
    emisor =  root[0] 
    receptor =  root[1]
    nomina = root[3][0]
    
    print(emisor.get('Nombre'), emisor.get('Rfc'))  
    print(nomina.get('FechaInicialPago'), nomina.get('FechaFinalPago'), nomina.get('NumDiasPagados'))
    print(nomina.get('TotalDeducciones'), nomina.get('TotalPercepciones'))  

    print("Percepciones")
    for k in range(len(root[3][0][2])):
        print(root[3][0][2][k].get('Concepto'), root[3][0][2][k].get('ImporteExento'), root[3][0][2][k].get('ImporteGravado'))

    print("Deducciones")
    for k in range(len(root[3][0][3])):
        print(root[3][0][3][k].get('Concepto'), root[3][0][3][k].get('Importe'))

    print("Otro Pagos")
    for k in range(len(root[3][0][4])):
        print(root[3][0][4][k].get('Concepto'), root[3][0][4][k].get('Importe'))



def main():
    args = parse_args()
    viewnom(args.filename)


if __name__ == '__main__':
   sys.exit(main())

