#! /usr/bin/env python

__version__ = "20210713.01"

import sys
import argparse
from tabulate import tabulate
import cx_Oracle
import os
import platform


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
    connection = None
    is_window = any(platform.win32_ver())
    db_user = os.environ.get("ORACLE_USER")
    db_dns = os.environ.get("ORACLE_CONN")
    db_pwd = os.environ.get("ORACLE_PWD")
    try:
        if is_window:
            cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\sqldeveloper\instantclient_19_11")
        connection = cx_Oracle.connect(user=db_user, password=db_pwd, dsn=db_dns)
        cursor = connection.cursor()
        if args.list:
            cursor.execute("select * from infonavit order by fecha, origen")
            list_data = cursor.fetchall()
            print(tabulate(list_data, floatfmt=".2f"))
        if args.fecha and args.trans and args.saldo:
            fecha = args.fecha
            cpto_id = '7001'
            concepto = 'SEGURO/COMISION'
            origen = '-'
            trans = args.trans
            seguro = trans
            interes = 0
            capital = 0
            saldo = args.saldo
            cursor.execute("insert into infonavit values (to_date(:fecha,'YYYY-MM-DD'), :concep_id, :concepto, :origen,"
                           " :trans, :seguro, :interes, :capital, :saldo)",
                           [fecha, cpto_id, concepto, origen, trans, seguro, interes, capital, saldo])
            connection.commit()
            print(tabulate([(fecha, cpto_id, concepto, origen, trans, seguro, interes, capital, saldo,
                             "Updated to Oracle DB.")]))
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
