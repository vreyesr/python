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
    parser.add_argument('-fo', '--fecha_oper', dest="fecha_oper", help="Specific a XML file")
    parser.add_argument('-fl', '--fecha_liq', dest="fecha_liq", help="Insert to postgres DB")
    parser.add_argument('-d', '--descripcion', dest="descrip", help="Insert to postgres DB")
    parser.add_argument('-r', '--referencia', dest="ref", help="Insert to postgres DB")
    parser.add_argument('-c', '--cargos', dest="cargos", help="Insert to postgres DB")
    parser.add_argument('-a', '--abonos', dest="abonos", help="Insert to postgres DB")
    parser.add_argument('-o', '--operacion', dest="oper", help="Insert to postgres DB")
    parser.add_argument('-q', '--liquidacion', dest="liq", help="Insert to postgres DB")


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
            cursor.execute("select * from bancomer order by oper, liq")
            list_data = cursor.fetchall()
            print(tabulate(list_data, floatfmt=".2f"))
        if args.oper and args.liq and args.descrip:
            cta =  os.environ.get("CTA")
            clabe = os.environ.get("CALBE")
            f_oper = args.fecha_oper
            f_liq =  args.fecha_liq
            descrip = args.descrip
            refer = args.ref
            cargo = args.cargos
            abono = args.abonos
            operacion = args.oper
            liquidacion = args.liq
            cursor.execute("insert into bancomer values (:cuenta, :clabe, to_date(:oper,'YYYY-MM-DD HH24:MI'), to_date(:liq,'YYYY-MM-DD HH24:MI'), :descripcion, :referencia, :cargos,"
                           " :abonos, :operacion, :liquidacion)",
                           [cta, clabe, f_oper, f_liq, descrip, refer, cargo, abono, operacion, liquidacion])
            connection.commit()
            print(tabulate([(cta, clabe, f_oper, f_liq, descrip, refer, cargo, abono, operacion, liquidacion)]))
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
