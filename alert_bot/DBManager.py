# -*- coding: utf-8 -*-
"""
@author: xeng
"""

#sudo service postgresql start
#sudo service postgresql stop
import psycopg2
import os
import urlparse




class DBManager():
    
    
    def __init__(self):
        try:
            con = self.heroku_connect()
            #con = psycopg2.connect(database='testdb', user='xeng')
            cur = con.cursor()
        except:
            print("----------------Error. Could not connect to database.---------")
            os._exit(1)
            
            
        self.subscribers = []
        self.commentID = []

        
        self.fetch_table()

        
    
    def create_table(self):
        try:
            con = self.heroku_connect()
            #con = psycopg2.connect(database='testdb', user='xeng')
            cur = con.cursor()
            cur.execute("SELECT * from Subscribers")
            con.commit()
            con.close()

        #If somehow database could not work, new one is created?
        except:
            con = self.heroku_connect()
            #con = psycopg2.connect(database='testdb', user='xeng')
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS Subscribers")
            cur.execute("CREATE TABLE Subscribers(Name TEXT, CommentID TEXT[])")

            con.commit()
            con.close()
            print("Error loading in database.")
            os._exit(1)
        
    
    
    def print_table(self):

            
        try:
            con = self.heroku_connect()
            #con = psycopg2.connect(database='testdb', user='xeng')
            cur = con.cursor()
            cur.execute("SELECT * from Subscribers ")
            row = cur.fetchall()
                
            print('\n')
            for x in row:
                print(x)
                print('\n')
            con.commit()
            con.close()
    
        except:
            print("Could not print table!")
            os._exit(1)
           
            
            
    def fetch_table(self):
        try:
            con = self.heroku_connect()
            #con = psycopg2.connect(database='testdb', user='xeng')
            cur = con.cursor()
            cur.execute("SELECT * from Subscribers ")
        
            row = cur.fetchall()
            
            for x in row:
                
                self.subscribers.append(x[0])
                self.commentID.append(x[1])

        except:
            print("Could not fetch database!")
            os._exit(1)
            
    #adding subscribers to the list.
    def add_subs(self, to_add):
        
        
        for x in to_add:
            try:
                con = self.heroku_connect()
                #con = psycopg2.connect(database='testdb', user='xeng')
                cur = con.cursor()    
    
                cur.execute("INSERT INTO Subscribers VALUES('%s', '{}')" % str(x))
                con.commit()
                con.close()
    
            except:
                print("Unable to add subscriber. add_subs()")
                pass
    
    
    #deletinga subscribers from the list.
    def del_subs(self, to_delete):
        
        for x in to_delete:
            try:
                con = self.heroku_connect()
                #con = psycopg2.connect(database='testdb', user='xeng')
                cur = con.cursor()
                
                cur.execute("DELETE FROM Subscribers WHERE Name = '%s'" % str(x))
                
                con.commit()
                con.close()
            except:
                print("Could not remove subscriber. del_subs()")
                pass
        
        
    
    #All the comments in comment_array are suppose to be new.   
    #Only the user 'habnpam' get's the id of the comments.     
    def update_commentHistory(self, comment_array):

        #print("Number of new comments: " + str(len(comment_array)))
        try:
            for x in comment_array:
                comment_link = str(x)
                con = self.heroku_connect()
                #con = psycopg2.connect(database='testdb', user='xeng')
                cur = con.cursor()

                
                cur.execute("""UPDATE Subscribers SET CommentID = array_append(CommentID, '%s') WHERE Name='habnpam'""" % (str(comment_link)))
                con.commit()
                con.close()
        except:
            print("Could not update the comments. update_commentHistory() in DBManager.")
            pass
        

    def remove_old_comments(self, old):
        
        for x in old:
            print("Removing comments/submissions history...")
            print(x)
            try:
                con = self.heroku_connect()
                #con = psycopg2.connect(database='testdb', user='xeng')
                cur = con.cursor()
                
                #Without specifying the "WHERE", every array in the CommentID column
                #should be affected.
                cur.execute("""UPDATE Subscribers SET CommentID = array_remove(CommentID, '%s')""" % (str(x)))
                
                con.commit()
                con.close()
            except:
                print("Could not remove old comments. remove_old_comments().")
                pass


    #Connect to the database on Heroku.
    def heroku_connect(self):
        urlparse.uses_netloc.append("postgres")
        
        url = urlparse.urlparse(url=os.environ['DATABASE_URL'])

        con = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port)
                

        return con
#=====================================================================
#
#                       The Database is set up like this:
#
#=====================================================================           
#
#       Name    |      Comment Link
#-------------------------------------
# Subscriber1   |   ['comment1.permalink', 'comment2.permalink', etc]
# Subscriber2   |
# Subscriber3   |
# Subscriber4   |
# Subscriber5   |
# Subscriber6   |
# Subscriber7   |
# Subscriber8   |
# Subscriber9   |
# Subscriber0   |
#
#
#
#
#=========================================================================