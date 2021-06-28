#!/usr/bin/python3

import cx_Oracle
import psycopg2
from tabulate import tabulate
import datetime
import argparse
import sys
import os



def parse_args():
    parser = argparse.ArgumentParser(prog="up_exp.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Database reports for LibreNMS and SWR")

    parser.add_argument('-l', '--dblist', action="store_true", help="Specific a Year use YYYY")
    parser.add_argument('-q', '--query', action="store_true", help="Specific a Year use YYYY")
    parser.add_argument('-e', '--expense_id', dest="exp_id", help="Specific a RFC")
    parser.add_argument('-v', '--value', dest="value", help="Specific a RFC")
    parser.add_argument('-c', '--comm', dest="comm", help="Specific a RFC")
    parser.add_argument('-o', '--oracle', action="store_true", help="Specific a RFC")
    parser.add_argument('-p', '--postgres', action="store_true", help="Specific a RFC")

    local_args = parser.parse_args()

    try:
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
    except Exception:
        sys.exit(1)

    return local_args



def db_postgres(pgquery=None, exp_id=None, value=None, comm=None):
    con = None
    current_ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pg_user =  os.environ.get("POSTGRES_USER")
    pg_host =  os.environ.get("POSTGRES_HOST")
    pg_db =  os.environ.get("POSTGRES_DB")
    pg_pwd =  os.environ.get("POSTGRES_PWD")
    try:
        con = psycopg2.connect(database=pg_db, user=pg_user, host=pg_host, password=pg_pwd)
        cur = con.cursor()
        if pgquery:
            cur.execute("select * from fnz_data.expenses2 order by fecha") 
            print(tabulate(cur.fetchall()))
        #cur.execute("select * from fnz_data.expenses2 values (%s,%s,%s,%s,%s,%s,%s)", [x[7], x[0], x[1], x[2], dia, per, ded ])

        if exp_id and value and comm:
            print(exp_id, value,comm)
            print([int(exp_id), current_ts, int(value), comm])
            cur.execute("insert into fnz_data.expenses2 values (%s, %s, %s, %s)", 
                           [int(exp_id), current_ts, int(value), comm ])
            con.commit()

    except psycopg2.DatabaseError as e:
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if con:
            con.close()



def db_oracle(dblist=None, query=None, exp_id=None, value=None, comm=None):
        current_ts = datetime.datetime.now().strftime('%d-%b-%y %H:%M:%S')
        connection = None
        db_user = os.environ.get("ORACLE_USER")
        db_dns =  os.environ.get("ORACLE_CONN")
        db_pwd =  os.environ.get("ORACLE_PWD")
        try:
            c=[]
            #cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\sqldeveloper\instantclient\instantclient_19_11")

            connection = cx_Oracle.connect(user=db_user, password=db_pwd, dsn=db_dns)
            cursor = connection.cursor()
            if dblist:
                cursor.execute("select * from exp_cpto") 
                list_data = cursor.fetchall()
                print(tabulate(list_data))
            if query:
                cursor.execute("select a.fecha, b.concepto, a.cant, a.commentario from expenses a, exp_cpto b where a.cpto_id = b.cpto_id order by fecha") 
                list_data = cursor.fetchall()
                print(tabulate(list_data))
            if exp_id and value and comm:
                print([int(args.exp_id), current_ts, int(args.value), args.comm])
                cursor.execute("insert into expenses values (:cpto_id, :fecha, :cant, :commentario)", 
                               [int(args.exp_id), current_ts, int(args.value), args.comm ])
                connection.commit()

        except cx_Oracle.DatabaseError as e:
            print('Error %s' % e)
            sys.exit(1)
        finally:
            if connection:
                connection.close()


def main():
    args = parse_args()
    if args.oracle and args.dblist:
        db_oracle(dblist=True)
    elif args.oracle and args.query:
        db_oracle(query=True)
    elif args.oracle and args.exp_id and args.value and args.comm:
        db_oracle(exp_id=args.exp_id, value=args.value, comm=args.comm)

    if args.postgres and args.query:
        db_postgres(pgquery=True)

    if args.postgres and args.exp_id and args.value and args.comm:
        db_postgres(exp_id=args.exp_id, value=args.value, comm=args.comm)


if __name__ == '__main__':
    sys.exit(main())

