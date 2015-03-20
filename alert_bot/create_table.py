# -*- coding: utf-8 -*-
"""
@author: xeng
"""
import psycopg2
import sys
import os
import urlparse

def heroku_connect():
    urlparse.uses_netloc.append("postgres")
        
    url = urlparse.urlparse(url=os.environ['DATABASE_URL'])

    con = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
                

    return con
    
    
con = None

try:
    #con = psycopg2.connect(dbname='testdb', user='xeng')
    con = heroku_connect()
    cur = con.cursor()    
    
    cur.execute("DROP TABLE IF EXISTS Subscribers")
    cur.execute("CREATE TABLE Subscribers(Name TEXT, CommentID TEXT[])")

    con.commit()
    print("Database table deleted and new one created!")

except:
    print("WE HAVE AN ERROR")
    
    
    
finally:
    if con:
        con.close()
