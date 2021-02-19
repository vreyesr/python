from lxml import etree
from decimal import *
import os
import fnmatch
import sys
from datetime import datetime
import sqlite3
import argparse
from tabulate import tabulate


def get_files(year):
    dir = "D:/finanazas/impuestos/shcp/Facturas/{0}/".format(year)
    return [os.path.join(dir, f) for f in os.listdir(dir) if fnmatch.fnmatch(f, '*.xml')]


def list_f(year):
    list_fac = []
    filter_list = []
    #     db =  sqlite3.connect(':memory:')
    #     cursor = db.cursor()
    #     cursor.execute('''CREATE TABLE fac(fecha date, rfc TEXT, name TEXT, desc TEXT, total integer)''')
    #     db.commit()
    #     con=0
    #     cursor = db.cursor()
    #     if len(sys.argv) == 2:
    #     print("--- %s ----" %sys.argv[1])
    file_err = []
    for i in get_files(year):
        try:
            root = etree.parse(i).getroot()
            if year >= '2019':
                v_fec = root.get("Fecha")
                v_rfc = root[0].get('Rfc')
                v_name = root[0].get("Nombre")
                v_desc = root[2][0].get('Descripcion')
                v_total = root.get("Total")
            else:
                v_fec = root.get("fecha")
                v_rfc = root[0].get('rfc')
                v_name = root[0].get("nombre")
                v_desc = root[2][0].get('descripcion')
                v_total = root.get("total")
            if v_fec or v_rfc or v_name or v_desc or v_total:
                list_fac.append((v_fec, v_rfc, v_name, v_desc, v_total, i[-9:]))
        except IndexError:
            file_err.append(i)
    for i in file_err:
        root = etree.parse(i).getroot()
        v_fec = root.get("Fecha")
        v_rfc = root[1].get('Rfc')
        v_name = root[1].get("Nombre")
        v_desc = root[3][0].get('Descripcion')
        v_total = root.get("Total")
        if v_fec or v_rfc or v_name or v_desc or v_total:
            list_fac.append((v_fec, v_rfc, v_name, v_desc, v_total, i[-9:]))
    if args.exclude:
        filter_list = [x for x in list_fac if args.exclude not in x[2]]
        filter_list.append(("=== TOTAL ===", " ", " ", " ", sum([float(x[4]) for x in filter_list])))
        return filter_list
    if args.rfc:
        filter_list = [x for x in list_fac if args.rfc.upper() in x[1]]
        filter_list.append(("=== TOTAL ===", " ", " ", " ", sum([float(x[4]) for x in filter_list])))
        return filter_list
    if args.mes:
        mes_list = [x for x in list_fac if args.mes in x[0].split('-')[1]]
        mes_list.append(("=== TOTAL ===", " ", " ", " ", sum([float(x[4]) for x in mes_list])))
        return mes_list
    list_fac.append(("=== TOTAL ===", " ", " ", " ", sum([float(x[4]) for x in list_fac])))
    return list_fac
    # cursor.execute('''INSERT INTO fac(fecha, rfc,name,desc,total) values (?,?,?,?,?)''',(v_fec,v_rfc,v_name,v_desc,v_total))
    # db.commit()
    # ursor.execute('select fecha,rfc,name,count(*),sum(total) from fac group by rfc order by fecha')
    # suma=0
    # for row in cursor:
    # print("%-s %-14s %-80s (%+3s) %9.2f" %(row[0],row[1],row[2],row[3],row[4]))
    # suma += row[3]
    # print("%111d===" %suma)
    # cursor.execute('delete from fac')
    # db.commit()

def rfc_f():
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    #cursor.execute('''CREATE TABLE fac(fecha date, rfc TEXT, name TEXT, desc TEXT, total integer)''')
    db.commit()
    rfc = str(sys.argv[2])
    v_total=0
    con=0
    for i in get_files(dir):
        root=etree.parse(i).getroot()
        v_fec=datetime.strptime(root.attrib["fecha"][0:10], '%Y-%m-%d').date()
        v_rfc=root[0].attrib["rfc"]
        v_name=root[0].attrib["nombre"]
        v_desc=root[2][0].attrib["descripcion"]
        v_total=root.attrib["total"]
        if root[0].attrib["rfc"] == rfc:
            cursor.execute('''INSERT INTO fac(fecha, rfc,name,desc,total) values (?,?,?,?,?)''',(v_fec,v_rfc,v_name,v_desc,v_total))
            db.commit()
        cursor.execute('select fecha,rfc,name,desc,total from fac order by fecha')
        suma=0
        for row in cursor:
            print("%-s %-14s %-40s (%-90s) %9.2f" %(row[0],row[1],row[2],row[3],row[4]))
            suma += row[4]
        print("%169.2f===" %suma)
        cursor.execute('delete from fac')
        db.commit()
    # sum = Decimal(root.attrib["total"])
    # v_total += sum
    # o=datetime.strptime(root.attrib["fecha"][0:10], '%Y-%m-%d').date(), root[2][0].attrib["descripcion"], root[0].attrib["nombre"], root.attrib["total"]
    # print "%+4s" %con,"%-15s" %o[0],"%-30s" %o[1], "%-30s" %o[2], "%+40s" %o[3]
    # con += 1
# print "%+4s == %+90s %9.2f ===" %(con," ",v_total)


def parse_args():
    parser = argparse.ArgumentParser(prog="facturas.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Database reports for LibreNMS and SWR")

    parser.add_argument('-y', '--year', dest="year", help="Specific a Year use YYYY")
    parser.add_argument('-r', '--rfc', dest="rfc", help="Specific a RFC")
    parser.add_argument('-m', '--mes', dest="mes", help="Specific a RFC")
    parser.add_argument('-x', '--exclude', dest="exclude", help="Specific a RFC")

    args = parser.parse_args()

    try:
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
    except Exception:
        sys.exit(1)

    return args



if __name__ == "__main__":
    args = parse_args()
    print(tabulate(sorted(list_f(args.year), key=lambda x: (x[0], x[1]) ), floatfmt=",.2f", numalign="right", showindex=True))

    '''
    if len(sys.argv) == 
        print(tabulate(sorted(list_f(args.year), key=lambda x: (x[0], x[1]) ), floatfmt=".2f", showindex=True))
    if len(sys.argv) == 3:
        print(tabulate(sorted([x for x in list_f() if str(sys.argv[2]).upper() in x[1] ], key=lambda x: (x[0],x[1]) )))
        print('Total','','','',sum([float(x[4]) for x in list_f() if str(sys.argv[2]).upper() in x[1] ]))
    '''
