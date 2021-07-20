#! /usr/bin/env python
import time


def get_fecha(b_fecha, year='2012'):
    dia = b_fecha.split('/')[0]
    mes = b_fecha.split('/')[1]
    min = time.localtime().tm_min
    sec = time.strftime('%S',time.localtime())
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
     'DIC': '12' }
    
    return str("{0}-{1}-{2} 12:{3}".format(year,anio[mes],dia, sec))

def get_file_format():
    t=[]
    l=[]
    l1=[]
    f=open(r'D:\test.txt', 'r')
    d=f.readlines()
    a= [x.strip() for x in d if x.strip()]
    for k in a:
        if len(k) == 6 and 'JUN' in k or 'JUL' in k and k.split('/')[0].isdigit():

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
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split()[0], x[4].split()[1] + ' ' + x[4].split()[2], '0', x[3] , '0', '0' ] for x in final if 'SPEI' in x[2] and not 'MEXICO' in x[4] if len(x) == 5 ])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split('CV')[0], x[4].split('CV')[1].lstrip(), '0', x[3] , '0', '0' ] for x in final if 'SPEI' in x[2] and 'MEXICO' in x[4] and len(x) == 5 ])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[6].split()[0] + ' ' + x[6].split()[1] + ' ' + x[6].split()[2], x[6].split()[3], x[3],'0', x[4] ,x[5] ] for x in final if 'TRASP' in x[2] and len(x) == 7])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split()[0] + x[4].split()[1], x[4].split()[2],  x[3], '0', '0', '0' ] for x in final if len(x) == 5 and 'SPEI' not in x[2] and 'AMERICAN' in x[2]])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split('BNET')[0] + 'BNET', x[4].split('BNET')[1].lstrip(), x[3], '0', '0', '0' ] for x in final if len(x) == 5 and 'CANAL' in x[4] and 'COMPRA' in x[2]])
    deploy.extend([[x[0],x[1],x[2] + ' ' + x[4].split('BNET')[0] + 'BNET', x[4].split('BNET')[1].lstrip(), '0', x[3], '0', '0' ] for x in final if len(x) == 5 and 'CANAL' in x[4] and 'VENTA' in x[2]])
    #for k in deploy:
    #    print(k)
    return deploy



if __name__ == '__main__':

    print(get_file_format())

    list_result=[]
    for x in get_file_format():
        list_result.append((get_fecha(x[0]),
                            get_fecha(x[1]),
                            x[2],
                            str(x[3]),
                            float(x[4]),
                            float(x[5]),
                            float(x[6]),
                            float(x[7])))  # for x in list_result])
        time.sleep(1)
    for k in list_result.sorted():
        print(k)

    '''
    list_result=[]
    insert_list = []
    with open(r'D:\test.txt') as f:
        list_result.extend(f.readlines())
    print(len(list_result), [len(x.split(',')) for x in list_result])
    for x in list_result:
        insert_list.append((get_fecha(x.split(',')[0]),
                             get_fecha(x.split(',')[1]),
                             x.split(',')[2].lstrip(),
                             str(x.split(',')[3].lstrip()),
                             float(x.split(',')[4]),
                             float(x.split(',')[5]),
                             float(x.split(',')[6]),
                             float(x.split(',')[7]))) #for x in list_result])
        time.sleep(1)

    print(insert_list)
    for k in insert_list:
        print(k)
    #for d in ['16/MAY', '23/MAY', '30/MAY', '31/MAY', '02/JUN', '13/JUN', '13/JUN']:
    #    print(get_fecha(d,'2013'))
    #   time.sleep(1)
    '''
