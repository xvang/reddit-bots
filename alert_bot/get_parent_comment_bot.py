import praw
import os
import time
import calendar
import copy

from DBManager import DBManager


class Stalker:
    
    def __init__(self):
        self.sub_keyword = "subscribe"                       #keyword to subscribe.
        self.unsub_keyword = "stop"                          #keyword to unsubscribe.
        
        self.verify_string = "Confirmed: 1 delta awarded to" #checks deltaBot's comment for this 
                                                             #string to see if delta was awarded.       
        
        self.target_user = os.environ['TARGET_USER']                         #targeted user.
       
        self.subscribers = []
        self.commentID = []
        
        self.dbManager = DBManager()

        self.new_subs = []
        self.stop_subs = []
    
        self.new_comments = []#Stores new comment Objects.  
        
        self.expired_comments = []#Stores old comment IDs to be deleted.
        
        self.r = None

        try:
            self.r = praw.Reddit(user_agent=os.environ['BOTNAME'])
            self.r.login(username=os.environ['USERNAME'], password=os.environ['PASSWORD'])
        except:
            print("Could not log in class Stalker __init__()")
            os._exit(0)
        
        
        
    def run(self):
        self.load_in_database()
        self.check_comments()
        self.check_mail()
    
        #Checks for old comments.(older than 1 week)
        self.determine_old_comments()

        self.dbManager.update_commentHistory(comment_array=self.new_comments)
        self.dbManager.add_subs(to_add=self.new_subs)
        self.dbManager.del_subs(to_delete=self.stop_subs)
        
        self.dbManager.remove_old_comments(old=self.expired_comments)

        print("Subscribers: " + str(self.subscribers))
        self.reset()
        
        
    #resetting the arrays.
    #Not 100% sure it is required, but better safe than sorry? Maybe?
    def reset(self):
        self.subscribers[:] = []
        self.commentID[:] = []
    
        self.new_subs[:] = []
        self.stop_subs[:] = []
        self.new_comments[:] = []
        self.expired_comments[:] = []
        
        
        self.dbManager = DBManager()


        
    #Passes the 2 arrays containing names to add / delete to the DBManager object.
    def update_database(self):
        self.dbManager.add_subs(to_add=self.new_subs)
        self.dbManager.del_subs(to_delete=self.stop_subs)
        
    
    def load_in_database(self):
        self.subscribers = copy.copy(self.dbManager.subscribers)
        self.commentID = copy.copy(self.dbManager.commentID)


    #Sends a message to subscribers.
    def send_message_to_subscribers(self, url):
        m = 'Link to the comment that changed someone\'s view: '
        e = str(url)
        s = '\n\n'
        a = "\n\n  ---  \n \n ^^To ^^unsubscribe, ^^send  ^^\"unsubscribe\" ^^message ^^to ^^/u/[name]"

        message = m + e + s + a 
        
        for sub in self.subscribers:
            try:
                self.r.send_message(sub, "Another View Changed in /r/CMV.", message)
            except:
                print("could not send to user: " + sub)
                pass


    #if the comment contained the string below, then a delta must have been awarded.
    #Then we must alert the subscribers.
    #The try-catch is there just to be safe.
    def gave_out_delta_thing(self, single_comment):
        try:
            return self.verify_string in single_comment.body
        except:
            print("Could not verify delta. gave_out_delta_thing()")
            return False


    def check_comments(self):
        #Retrieves comments from the bot that gives out delta things.
        comments = self.r.get_redditor(self.target_user).get_comments(sort='new', time='today', limit=10)
        
        for x in comments:
            #If bot gave out delta
            if (self.gave_out_delta_thing(single_comment = x)):
                parent = self.r.get_info(thing_id=x.parent_id)
                
                try:
                    #Loop until we get the top level comment where delta was given.
                    while not parent.is_root:
                        parent = self.r.get_info(thing_id=parent.parent_id)
                        time.sleep(3)

                    #print("parent.permalink = " + str(parent.permalink) + "\n")
                    #print("self.commentID[0] = " + str(self.commentID[0]) + "\n")
                    #If the top level comment's ID is not recognized, then it is new. We will alert the subscribers!
                    if(str(parent.permalink) not in self.commentID[0]):
                        print("New delta-awarded comment detected!")
                        self.send_message_to_subscribers(url=parent.permalink)
                        self.new_comments.append(parent.permalink)                    
                        time.sleep(5)
                        
                    else:
                        pass
                        #print("Comment awarded delta, but has already been alerted.")
                except:
                    #print("Post was not a comment reply. parent.is_root() failed.")
                    pass
            
            else:
                pass
                #print("Comment did not award delta")

    def check_mail(self):
        #Retrieve the unread messages.
        new_message = self.r.get_unread()
        
        
        for message in new_message:
            
            #Checks for the word "subscribe".
            #If True, then user will be added to subsriber list.
            body = str(message.body).lower()
            if self.sub_keyword in body:
                
                #Checks if the user requesting "subscribe" is a new subscriber.
                if str(message.author) not in self.subscribers and str(message.author) not in self.new_subs:
                    self.new_subs.append(str(message.author))#add to list that will get added to database.
                    
                    try:
                        print("New subscriber detected: " + str(message.author))
                        self.r.send_message(message.author, "Thank you for subscribing to deltabot_stalker!", ".")
                    except:
                        print("Could not send congratulatory message to new Subscriber!")
                        pass
                
            elif self.unsub_keyword in body:
                
                if str(message.author) in self.subscribers and str(message.author) not in self.stop_subs:
                    self.stop_subs.append(str(message.author))#added to list the will get removed from database.
                    
                    try:
                        print("Someone un-subscribed: " + str(message.author))
                        self.r.send_message(message.author, "You have unsubscribed from deltabot_stalker", ".")
                    except:
                        print("Could not send Unsubscribed message to subscriber!")
                        
            message.mark_as_read()
  

    #Determine which comments are old and should be removed.
    def determine_old_comments(self):
        
        try:
            #The first element of commentID should contain all the comments replied to already.
            all_comments = list(self.commentID[0])

            for x in all_comments:

                try:
                    
                    #retrieve the comment using the ID
                    comment = self.r.get_submission(submission_id=str(x))
                    
                    #get the time comment was created.
                    #I believe it is since Epoch (in seconds)
                    created_time = comment.comments[0].created_utc
                   
                   
                    #get the time now.
                    time_now = calendar.timegm(time.gmtime())
                    
                    
                    #"age" of the comment.
                    age_limit = time_now - created_time
                    
                    
                    #print("Comment's age = " + str(age_limit))
                    #There are about 604800 seconds in a week.
                    #If comment is older than that, 
                    #then its comment Id will be deleted from database.
            
                    if(age_limit >= 604800):
                        print("FOUND AN OLD COMMENT!")
                        self.expired_comments.append(str(x))
                        
                    
                #If the comment was deleted, then errors would show up
                #when we execute get_submission().
                except:
                    print("Somehow comment ID became corrupted. It will be deleted!")
                    self.expired_comments.append(str(x))
                    pass
                
                all_comments[:] = []
                
        except:
            print("Could not do anything in remove_old_comments()!")
            pass
            
    
#====================================================================================#
#                          END OF CLASS DECLARATION                                  #
#====================================================================================#                





def main():
    stalker = Stalker()
    
    while(True):
        stalker.run()
        
        print("Finished. Sleeping now. 10 minutes.")
        time.sleep(600)



if __name__ == '__main__':
    main()
