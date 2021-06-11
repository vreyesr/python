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
    parser.add_argument('-d', '--database', action="store_true", help="Insert to postgres DB")
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
    nomina_data = root[3][0]
    num_empleado = nomina_data[1].get('NumEmpleado')
    fecha_inicial = nomina_data.get('FechaInicialPago')
    fecha_final = nomina_data.get('FechaFinalPago')
    dias = nomina_data.get('NumDiasPagados')
    
    print(tabulate([(emisor.get('Nombre'), emisor.get('Rfc'))], tablefmt="plain"))
    print(tabulate([(receptor.get('Nombre'), receptor.get('Rfc'), nomina_data[1].get('Curp'), nomina_data[1].get('NumSeguridadSocial'), nomina_data[1].get('Puesto'))], tablefmt="sql"))
    total = []
    headers = ['# Emp', 'F. Inicial', 'F. Final', 'Dias', 'Percepciones', 'Deducciones', 'Concepto', 'Clave']
    #print(nomina_data.get('FechaInicialPago'), nomina_data.get('FechaFinalPago'), nomina_data.get('NumDiasPagados'))
    #print(nomina_data.get('TotalDeducciones'), nomina_data.get('TotalPercepciones'))  

    #print("Percepciones")
    for k in range(len(root[3][0][2])):
       importe_gravado = float(root[3][0][2][k].get('ImporteGravado'))
       importe_exento = float(root[3][0][2][k].get('ImporteExento'))
       if float(root[3][0][2][k].get('ImporteGravado')) > 0:
           #total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:,.2f}".format(importe_gravado), '-', root[3][0][2][k].get('Concepto').split('_')[1], root[3][0][2][k].get('Concepto').split('_')[0]))
           total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:.2f}".format(importe_gravado), '-', root[3][0][2][k].get('Concepto').split('_')[1], root[3][0][2][k].get('Concepto').split('_')[0]))
       if float(root[3][0][2][k].get('ImporteExento')) > 0:
           #total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:,.2f}*".format(importe_exento), '-', root[3][0][2][k].get('Concepto').split('_')[1], root[3][0][2][k].get('Concepto').split('_')[0]))
           total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:.2f}".format(importe_exento), '-', root[3][0][2][k].get('Concepto').split('_')[1], root[3][0][2][k].get('Concepto').split('_')[0]))
    #print(tabulate(total))

    #print("Deducciones")
    for k in range(len(root[3][0][3])):
        importe = float(root[3][0][3][k].get('Importe'))
        #print(('-', root[3][0][3][k].get('Importe'), root[3][0][3][k].get('Concepto').split('_')[1], root[3][0][3][k].get('Concepto').split('_')[0] ))
        #total.append((num_empleado, fecha_inicial, fecha_final, dias, '-', "{:,.2f}".format(importe), root[3][0][3][k].get('Concepto').split('_')[1], root[3][0][3][k].get('Concepto').split('_')[0] ))
        total.append((num_empleado, fecha_inicial, fecha_final, dias, '-', "{:.2f}".format(importe), root[3][0][3][k].get('Concepto').split('_')[1], root[3][0][3][k].get('Concepto').split('_')[0] ))
    #print(tabulate(total))

    #print("Otro Pagos")
    for k in range(len(root[3][0][4])):
        otro_importe = float(root[3][0][4][k].get('Importe'))
#        print(root[3][0][4][k].get('Concepto'), root[3][0][4][k].get('Importe'))
        #total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:,.2f}".format(otro_importe), '-',  root[3][0][4][k].get('Concepto').split('_')[1], root[3][0][4][k].get('Concepto').split('_')[0]))
        total.append((num_empleado, fecha_inicial, fecha_final, dias, "{:.2f}".format(otro_importe), '-',  root[3][0][4][k].get('Concepto').split('_')[1], root[3][0][4][k].get('Concepto').split('_')[0]))
    #print(tabulate(total, floatfmt=("","","",",.2f",",.2f"), colalign=("","","","right","right","right")))
    #print(tabulate(total, floatfmt=("","","",",.2f",",.2f"), colalign=("","","","right","right","right")))
	#print(tabulate(sorted(total, key=lambda x: x[6]), floatfmt=".3f", numalign="right"))
    
    return total
    #print(tabulate(sorted(total, key=lambda x: x[7]), stralign="right", headers= headers))
  
    #print([(int(x[7]), x[0], x[1], x[2], int(float(x[3])), float(x[4].replace('-','0')), float(x[5].replace('-','0'))) for x in total])


def db_postgres(list_fac):
    con = None
    try:
        con = psycopg2.connect(database='vbrr_db', user='postgres', host='192.168.15.99', password='kmslit299')
        cur = con.cursor()
        for x in list_fac:
            dia = int(float(x[3]))
            per = x[4].replace('-','0')
            ded = x[5].replace('-','0')
            cur.execute("insert into fnz_data.nomina values (%s,%s,%s,%s,%s,%s,%s)", [x[7], x[0], x[1], x[2], dia, per, ded ])
            con.commit()

    except psycopg2.DatabaseError as e:
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if con:
            con.close()




def main():
    args = parse_args()
    headers = ['# Emp', 'F. Inicial', 'F. Final', 'Dias', 'Percepciones', 'Deducciones', 'Concepto', 'Clave']
    #viewnom(args.filename)
    print(tabulate(sorted(viewnom(args.filename), key=lambda x: x[7]), stralign="right", headers= headers))


if __name__ == '__main__':
   sys.exit(main())

