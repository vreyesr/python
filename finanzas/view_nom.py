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
    num_empleado = root[3][0][1].get('NumEmpleado')
    fecha_inicial = nomina.get('FechaInicialPago')
    fecha_final = nomina.get('FechaFinalPago')
    dias = nomina.get('NumDiasPagados')
    
    total = []
    headers = ['# Emp', 'F. Inicial', 'F. Final', 'Dias', 'Percepciones', 'Deducciones', 'Concepto', 'Clave']
    print(emisor.get('Nombre'), emisor.get('Rfc'))  
    print(nomina.get('FechaInicialPago'), nomina.get('FechaFinalPago'), nomina.get('NumDiasPagados'))
    print(nomina.get('TotalDeducciones'), nomina.get('TotalPercepciones'))  

    #print("Percepciones")
    for k in range(len(root[3][0][2])):
       importe_gravado = float(root[3][0][2][k].get('ImporteGravado'))
       importe_exento = float(root[3][0][2][k].get('ImporteExento'))
       if float(root[3][0][2][k].get('ImporteGravado')) > 0:
           total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:,.2f}".format(importe_gravado), '-', root[3][0][2][k].get('Concepto').split('_')[1], root[3][0][2][k].get('Concepto').split('_')[0]))
       if float(root[3][0][2][k].get('ImporteExento')) > 0:
           total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:,.2f}*".format(importe_exento), '-', root[3][0][2][k].get('Concepto').split('_')[1], root[3][0][2][k].get('Concepto').split('_')[0]))
    #print(tabulate(total))

    #print("Deducciones")
    for k in range(len(root[3][0][3])):
        importe = float(root[3][0][3][k].get('Importe'))
        #print(('-', root[3][0][3][k].get('Importe'), root[3][0][3][k].get('Concepto').split('_')[1], root[3][0][3][k].get('Concepto').split('_')[0] ))
        total.append((num_empleado, fecha_inicial, fecha_final, dias, '-', "{:,.2f}".format(importe), root[3][0][3][k].get('Concepto').split('_')[1], root[3][0][3][k].get('Concepto').split('_')[0] ))
    #print(tabulate(total))

    #print("Otro Pagos")
    for k in range(len(root[3][0][4])):
        otro_importe = float(root[3][0][4][k].get('Importe'))
#        print(root[3][0][4][k].get('Concepto'), root[3][0][4][k].get('Importe'))
        total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:,.2f}".format(otro_importe), '-',  root[3][0][4][k].get('Concepto').split('_')[1], root[3][0][4][k].get('Concepto').split('_')[0]))
    #print(tabulate(total, floatfmt=("","","",",.2f",",.2f"), colalign=("","","","right","right","right")))
    #print(tabulate(total, floatfmt=("","","",",.2f",",.2f"), colalign=("","","","right","right","right")))
    #print(tabulate(sorted(total, key=lambda x: x[6]), floatfmt=".3f", numalign="right"))
    print(tabulate(sorted(total, key=lambda x: x[7]), stralign="right", headers= headers))



def main():
    args = parse_args()
    viewnom(args.filename)


if __name__ == '__main__':
   sys.exit(main())

