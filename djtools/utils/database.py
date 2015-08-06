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
    return dic

def mysql_db(sql,db='default',select=False):
    hs = settings.DATABASES[db]['HOST']
    pt = settings.DATABASES[db]['PORT']
    us = settings.DATABASES[db]['USER']
    ps = settings.DATABASES[db]['PASSWORD']
    db = settings.DATABASES[db]['NAME']
    conn  = MySQLdb.connect(host=hs,port=int(pt),user=us,passwd=ps,db=db,use_unicode=True,charset="utf8")
    result = None
    if select:
        conn.query(sql)
        r = conn.store_result()
        result = r.fetch_row(maxrows=0)
    else:
        curr = conn.cursor()
        result = curr.execute(sql)
        conn.commit()
        curr.close ()

    conn.close ()
    return result

def row2dict(row):
    """
    Convert sqlalchemy row object to python dictionary

    or as a one liner:

    row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
    """
    d = {}
    if row:
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)

    return d

