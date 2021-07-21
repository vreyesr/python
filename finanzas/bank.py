#! /usr/bin/env python

__version__ = "20210713.01"

import sys
import argparse
from tabulate import tabulate
import cx_Oracle
import os
import time
import platform


def get_fecha(b_fecha, year='2015'):
    dia = b_fecha.split('/')[0]
    mes = b_fecha.split('/')[1]
    min = time.localtime().tm_min
    sec = time.strftime('%S', time.localtime())
    anio = {
        'ENE': '01',
        'FEB': '02',
        'MAR': '03',
        'ABR': '04',
        'MAY': '05',
        'JUN': '06',
        'JUL': '07',
        'AGO': '08',
        'SEP': '09',
        'OCT': '10',
        'NOV': '11',
        'DIC': '12'}

    return str("{0}-{1}-{2} 12:{3}".format(year, anio[mes], dia, sec))


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
    parser.add_argument('-db', '--db_import', action="store_true", help="Insert to postgres DB")
    parser.add_argument('-y', '--yes', action="store_true", help="Insert to postgres DB")
    parser.add_argument('-v', '--view', action="store_true", help="Insert to postgres DB")


    local_args = parser.parse_args()

    try:
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
    except Exception:
        sys.exit(1)

    return local_args


def get_file_format():
    t=[]
    l=[]
    l1=[]
    f=open(r'D:\test.txt', 'r')
    d=f.readlines()
    a= [x.strip() for x in d if x.strip()]
    for k in a:
        if len(k) == 6 and 'ENE' in k or 'FEB' in k or 'MAR' in k or 'ABR' in k or 'MAY' in k or 'JUN' in k or 'JUL' in k or 'AGO' in k or 'SEP' in k or 'OCT' in k or 'NOV' in k or 'DIC' in k and k.split('/')[0].isdigit():

            l.append(k)
            l1.append(k)
        else:
            l.append(k)

    #print(l)
    o=[]

    o=[x.replace('Referencia','') for x in l]
    z=[x.replace(',', '') for x in o]
    l=z
    #print(l)
    for c in l1:
       a=[i for i, e in enumerate(l) if e == c]
       t.extend(a)
    n=set(t)
    ind=[]
    for k,i in enumerate(n):
        if k % 2 == 0:
            ind.append(i)
    #print(ind, len(ind), ind[0],ind[1], ind[-1])
    final= []
    try:
        final.append((l[ind[0]:ind[1]]))
        final.append((l[ind[1]:ind[2]]))
        final.append((l[ind[2]:ind[3]]))
        final.append((l[ind[3]:ind[4]]))
        final.append((l[ind[4]:ind[5]]))
        final.append((l[ind[5]:ind[6]]))
        final.append((l[ind[6]:ind[7]]))
        final.append((l[ind[7]:ind[8]]))
        final.append((l[ind[8]:ind[9]]))
        final.append((l[ind[9]:ind[10]]))
        final.append((l[ind[10]:ind[11]]))
        final.append((l[ind[11]:ind[12]]))
        final.append((l[ind[12]:ind[13]]))
        final.append((l[ind[13]:ind[14]]))
        final.append((l[ind[15]:ind[15]]))
    except:
        pass
    final.append((l[ind[-1]:]))

    #for x in final:
    #    print(x)
    #print(len(final))
    deploy=[]
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[6].split()[0], x[6].split()[1] + ' ' + x[6].split()[2], x[3],'0', x[4] ,x[5] ] for x in final if 'TEF' in x[2] and len(x) == 7])
    # SPEI
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split()[0], x[4].split()[1] + ' ' + x[4].split()[2], '0', x[3] , '0', '0' ] for x in final if 'SPEI' in x[2] and not 'MEXICO' in x[4] if len(x) == 5 ])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split('CV')[0] + 'CV', x[4].split('CV')[1].lstrip(), '0', x[3] , '0', '0' ] for x in final if 'SPEI' in x[2] and 'MEXICO' in x[4] and len(x) == 5 ])
    # TRANSPASO
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[6].split()[0] + ' ' + x[6].split()[1] + ' ' + x[6].split()[2], x[6].split()[3], x[3],'0', x[4] ,x[5] ] for x in final if 'TRASP' in x[2] and len(x) == 7])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split()[0] + ' ' + x[4].split()[1] + ' ' + x[4].split()[2], x[4].split()[3], x[3], '0', '0', '0' ] for x in final if 'TRASP' in x[2] and len(x) == 5 ])

    # AMERICA
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split()[0] + ' ' + x[4].split()[1], x[4].split()[2], x[3], '0', '0', '0' ] for x in final if len(x) == 5 and 'SPEI' not in x[2] and 'AMERICAN' in x[2]])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[6].split()[0] + ' ' + x[6].split()[1], x[6].split()[2], x[3], '0', x[4] ,x[5] ] for x in final if len(x) == 7 and 'SPEI' not in x[2] and 'AMERICAN' in x[2]])
    # COMPRA & VENTA
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split('BNET')[0] + 'BNET', x[4].split('BNET')[1].lstrip(), x[3], '0', '0', '0' ] for x in final if len(x) == 5 and 'CANAL' in x[4] and 'COMPRA' in x[2]])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[6].split('BNET')[0] + 'BNET', x[6].split('BNET')[1].lstrip(), x[3], '0', x[4], x[5]] for x in final if len(x) == 7  and 'CANAL' in x[6] and 'COMPRA' in x[2]])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split('BNET')[0] + 'BNET', x[4].split('BNET')[1].lstrip(), '0', x[3], '0', '0' ] for x in final if len(x) == 5 and 'CANAL' in x[4] and 'VENTA' in x[2]])
    #for k in deploy:
    #    print(k)
    return deploy


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
            clabe = os.environ.get("CLABE")
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

        if args.view:
            print(len(get_file_format()))
            for k in get_file_format():
                print(k)

        if args.db_import:
            '''
            cta = os.environ.get("CTA")
            clabe = os.environ.get("CLABE")
            list_result = []
            insert_list = []
            #with open(r'D:\test.txt') as f:
            with open(r'/mnt/hgfs/D/test.txt') as f:
                list_result.extend(f.readlines())
            print(len(list_result), [len(x.split(',')) for x in list_result])
            '''
            cta = os.environ.get("CTA")
            clabe = os.environ.get("CLABE")
            list_result=[]
            for x in get_file_format():
                list_result.append((cta, clabe, get_fecha(x[0]),
                            get_fecha(x[1]),
                            x[2],
                            str(x[3]),
                            float(x[4]),
                            float(x[5]),
                            float(x[6]),
                            float(x[7])))
                time.sleep(1)
            insert_list = sorted(list_result, key=lambda x: x[2])
            print(len(insert_list), [len(x) for x in insert_list])
            for k in insert_list:
                print(k)

            '''
            insert_list = get_file_format()
            for k in insert_list:
                print(k)
            '''
            if args.yes:
                cursor.executemany("insert into bancomer values (:cuenta, :clabe, to_date(:oper,'YYYY-MM-DD HH24:MI'), to_date(:liq,'YYYY-MM-DD HH24:MI'), :descripcion, :referencia, :cargos,"
                    " :abonos, :operacion, :liquidacion)", insert_list)
                connection.commit()
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
