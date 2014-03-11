from django.conf import settings

import MySQLdb

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
