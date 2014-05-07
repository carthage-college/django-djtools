from django.conf import settings
from django.db import connections

import MySQLdb

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def do_mysql(sql,select=True,db="default"):
    dic = None
    cursor = connections[db].cursor()
    cursor.execute(sql)
    if select:
        dic = dictfetchall(cursor)
    cursor.close()
    return dic

def mysql_db(sql):
    hs = settings.DATABASES['livewhale']['HOST']
    us = settings.DATABASES['livewhale']['USER']
    ps = settings.DATABASES['livewhale']['PASSWORD']
    db = settings.DATABASES['livewhale']['NAME']
    conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db,use_unicode=True,charset="utf8")
    curr = conn.cursor()
    curr.execute(sql)
    conn.commit()
    curr.close ()
    conn.close ()
