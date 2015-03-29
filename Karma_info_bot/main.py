import praw
import pprint
import time
import datetime
import login

def run(bot):
    unread = bot.get_unread(limit=None)

    for message in unread:
        user = None
        target_user = ""

        
        #If message contains a "/u/", then the sender wants to check a user.
        if("/u/" in message.body):
            try:
                target_user = str(message.body).replace("/u/", "")
                user = bot.get_redditor(target_user)
                
            except:
                bot.send_message(message.author, "Invalid name", "Message should look like this: \n\n\n \"checkme\", or /u/name_of_user_ \n\n\n\n\n .....or it could be that the user does not exist. ")
                message.mark_as_read()
                return False

        #If message contains "checkme", then sender wants to check themself (themselves?).
        elif("checkme" in message.body):
            try:
                target_user = str(message.author)
                user = bot.get_redditor(target_user)
            except:
                bot.send_message(message.author, "Invalid name", "Message should look like this: \n\n\n \"checkme\", or /u/name_of_user_ \n\n\n\n\n .....or it could be that the user does not exist. ")
                message.mark_as_read()
                return False

        #get all the submissions of the user.
        gen = user.get_submitted(limit=None)

        karma_by_subreddit = {}

        #Records the start time for parsing through all the comments and submissions.
        start_time = time.time()
        
        for thing in gen:
            subreddit = thing.subreddit.display_name
            karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)

        #now we get all the comments made by the user.
        comments = user.get_comments(sort='top', time='all', limit=None)
        for c in comments:
            subreddit = c.subreddit.display_name
            karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + c.score)

        #stop time
        stop_time = time.time()

        elapsed_time = stop_time  - start_time

        #There has to be some module that takes "seconds" as an input and converts it to hours/minutes/seconds.
        #Find out ... later?
        minute = 0

        while(elapsed_time >= 60):
            minute = minute + 1
            elapsed_time = elapsed_time - 60

        #creating the message that will be returned.
        #It's kind of big, so I split it up into smaller strings.
        time_message = "Checking /u/" + str(target_user) + "'s stuff took: " + str(minute)  + " minutes, and " + str(round(elapsed_time,2)) + " seconds"

        #get the karma count.
        t_user = bot.get_redditor(target_user)
        karma_message = "Link Karma: " + str(t_user.link_karma) + "\n\n\nComment Karma: " + str(t_user.comment_karma)

        note_message = "\n\n\n\nNote: I think the max comments/submissions we can look at is 1000, so if a user made more than 1000 comments/submissions we can't get all of them." 

        note_message = note_message + "\n\nAnd I don't know why the points do not add up.  Points are weird."

        title_message = "##Karma Breakdown for /u/" + str(target_user) + "\n\n\n"

        subreddits_message = ""
        for key in karma_by_subreddit.keys():
            subreddits_message = subreddits_message + ("/r/%s: %s \n\n" %(key, karma_by_subreddit[key]))

        #putting all the strings together into one string.
        master_message = title_message + "\n\n" + karma_message + "\n\n" + time_message + "\n\n" + subreddits_message + "\n\n---\n\n" + note_message

        
        #Send a response message.
        bot.send_message(message.author, "Reply from Karma Breakdown Bot", master_message)

        #mark the message as "read"
        message.mark_as_read()
        
        print("Sent Reply to /u/" + str(message.author))




if __name__ == '__main__':

    #fetch the log in information from login.py
    login_info = login.login()

    r = praw.Reddit(login_info['botname'])
    r.login(login_info['name'],login_info['password'])
    
    while(True):
        run(bot = r)
        print("Sleeping. Alls is well.")
        time.sleep(30)
        











