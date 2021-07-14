#! /usr/bin/env python

__version__ = "20210713.01"

from lxml import etree
import os
import fnmatch
import sys
import datetime
import argparse
from tabulate import tabulate
import cx_Oracle


def parse_args():
    parser = argparse.ArgumentParser(prog="facturas.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Database reports for LibreNMS and SWR")

    parser.add_argument('-l', '--list', action="store_true", help="Specific a XML file")
    parser.add_argument('-f', '--fecha', dest="fecha", help="Insert to postgres DB")
    parser.add_argument('-s', '--seguro', dest="seguro", help="Insert to postgres DB")
    parser.add_argument('-t', '--trans', dest="trans", help="Insert to postgres DB")
    parser.add_argument('-d', '--saldo', dest="saldo", help="Insert to postgres DB")

    local_args = parser.parse_args()

    try:
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
    except Exception:
        sys.exit(1)

    return local_args




def db_oracle():
    args = parse_args()
    current_ts = datetime.datetime.now().strftime('%d-%b-%y %I:%M:%S')
    connection = None
    db_user = 'vbrr'  # os.environ.get("ORACLE_USER")
    db_dns = 'vbrrdb_high'  # os.environ.get("ORACLE_CONN")
    db_pwd = 'Lnx141501db$$'  # os.environ.get("ORACLE_PWD")
    try:
        c = []
        cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\sqldeveloper\instantclient_19_11")
        connection = cx_Oracle.connect(user=db_user, password=db_pwd, dsn=db_dns)
        cursor = connection.cursor()
        if args.list:
            cursor.execute("select * from infonavit order by fecha, origen")
            list_data = cursor.fetchall()
            print(tabulate(list_data, floatfmt=".2f"))
        if args.fecha and args.seguro and args.interes:
            fecha = args.fecha
            cpto_id = '7001'
            concepto = 'SEGURO/COMISION'
            origen = '-'
            trans =args.trans
            seguro = args.seguro
            interes = 0
            capital = 0
            saldo = args.saldo
            cursor.execute(
                "insert into expenses values (:fecha, :concep_id, :concepto, :origen, :trans, :seguro, :interes, :capital, :saldo)",
                [fecha, concepto, origen, trans, interes, capital, saldo])
            connection.commit()

        '''    
            if query:
                cursor.execute(
                    "select a.fecha, b.concepto, a.cant, a.commentario from expenses a, exp_cpto b where a.cpto_id = b.cpto_id order by fecha")
                list_data = cursor.fetchall()
                print(tabulate(list_data))
            if exp_id and value and comm:
                print([int(exp_id), current_ts, float(value), comm])
        '''
    except cx_Oracle.DatabaseError as e:
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if connection:
            connection.close()

def main():
    db_oracle()


if __name__ == '__main__':
    sys.exit(main())
