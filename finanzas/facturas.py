#! /usr/bin/python3

from lxml import etree
import os
import fnmatch
import sys
import argparse
from tabulate import tabulate
import psycopg2
import cx_Oracle
import os

__version__ = "20210622.01"


def get_files(year):
    try:
        # local_dir = "D:/finanazas/impuestos/shcp/Facturas/{0}/".format(year)
        local_dir =  os.environ.get("PATH_FACT") + "/" + year
        print(local_dir)
        return [os.path.join(local_dir, f) for f in os.listdir(local_dir) if fnmatch.fnmatch(f, '*.xml')]
    except FileNotFoundError:
        sys.exit("Please check directory is under 2013 and current year")


def list_f(year):
    list_fac = []
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
                list_fac.append((v_fec, v_rfc, v_name, v_desc, v_total, i[-40:][:8]))
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
            list_fac.append((v_fec, v_rfc, v_name, v_desc, v_total, i[-40:][:8]))
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

    if args.database:
        con = None
        try:
            con = psycopg2.connect(database='vbrr_db', user='postgres', host='192.168.15.99', password='')
            cur = con.cursor()
            for x in list_fac:
                id_db = (x[5].split(".")[0])
                cur.execute("insert into fnz_data.facturas values (%s,%s,%s,%s,%s,%s) on conflict do nothing", [
                    id_db, x[0], x[1], x[2], x[3], x[4]
                ])
            con.commit()

        except psycopg2.DatabaseError as e:
            print('Error %s' % e)
            sys.exit(1)
        finally:
            if con:
                con.close()

    if args.ocidb:
        connection = None
        try:
            cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\sqldeveloper\instantclient\instantclient_19_11")
            connection = cx_Oracle.connect(user="", password="", dsn="")
            cursor = connection.cursor()
            for x in list_fac:
                id_db = (x[5].split(".")[0])
                cursor.execute("insert into vbrr.facturas values (:file_id, to_timestamp(:fecha,'YYYY-MM-DD HH24:MI:SS'),:rfc,:nombre,:descrip, to_number(:total))", [
                    id_db, x[0].replace('T', ' '), x[1], x[2], x[3], x[4]
                ])
            connection.commit()

        except cx_Oracle.DatabaseError as e:
            print('Error %s' % e)
            sys.exit(1)
        finally:
            if connection:
                connection.close()


    list_fac.append(("=== TOTAL ===", " ", " ", " ", sum([float(x[4]) for x in list_fac])))
    return list_fac


def parse_args():
    parser = argparse.ArgumentParser(prog="facturas.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Database reports for LibreNMS and SWR",
                                     epilog = "Use the export PATH_FACT= variable")

    parser.add_argument('-y', '--year', dest="year", help="Specific a Year use YYYY")
    parser.add_argument('-r', '--rfc', dest="rfc", help="Specific a RFC")
    parser.add_argument('-m', '--mes', dest="mes", help="Specific a month 01 to 12")
    parser.add_argument('-x', '--exclude', dest="exclude", help="Exclude a Emisor name")
    parser.add_argument('-db', '--database', action="store_true", help="Store data to Postgres Database")
    parser.add_argument('-ocidb', '--ocidb', action="store_true", help="Store data to Oracle Database")

    local_args = parser.parse_args()

    try:
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
    except Exception:
        sys.exit(1)

    return local_args


if __name__ == "__main__":
    args = parse_args()
    print(tabulate(sorted(list_f(args.year), key=lambda x: (x[0], x[1])), floatfmt=",.2f", numalign="right",
                   showindex=True))
