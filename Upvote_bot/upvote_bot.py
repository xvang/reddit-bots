import praw
import time
from random import randint


'''
Upvote bot for reddit. Every so often, it chooses a random subreddit
from a list, and retrieves 20 newest threads and checks if
the comments in those threads have been mass downvoted.
The criteria for a mass downvote is >50% of all comments having zero or less karma
'''

class RedditBot():

    def __init__(self, parent=None):
        super(RedditBot, self).__init__()

        
    def login(self):
        self.r = praw.Reddit(user_agent='secret_mass_downvote_fighter_bot')
        self.r.login(self.login_name, self.login_pass)

        
    #this function "runs" the bot.
    #it gets a random subreddit from a list and gets the 10 new threads.
    def run(self):
        self.counter = self.counter + 1

        self.get_the_subreddit()
        print("Iteration#: " + str(self.counter) + "   Checking sub: " + str(self.sub.display_name))
        
        
        m = "Run #: " + str(self.counter) + "\n" + "Checking in sub: " + str(self.sub.display_name)

        self.r.send_message(self.boss, 'DVFB checking in', m)
        
        
        
        self.check_votes()
        
        

    def get_the_subreddit(self):
        self.sub_name = self.possible_subs[randint(0, len(self.possible_subs)-1)]
        self.sub = self.r.get_subreddit(self.sub_name)
   
        self.sub_threads = self.sub.get_new(limit = self.limit)
        
        


    def check_votes(self):

        for x in self.sub_threads:
            x.upvote()
            #resetting counters
            self.downvotes = 0
            
            comments = x.comments


            print("length of comment: " + str(len(comments)))
            if len(comments) < 10:
                for y in comments:
                    if(y.score <= 0):#this line is sometimes an error. Maybe some subreddits don't have upvotes and/or comments?
                        self.downvotes = self.downvotes + 1
            #If >50% of all comments had 0 karma, then someone(s? plural?) must have downvoted a bunch of comments.
            if(len(comments) > 0 and self.downvotes / len(comments) >= 0.5):
                for y in comments:
                    y.upvote()


                message = ("Found a mass downvote thread.\n" + "Subreddit: " + (self.sub.display_name) + "\n" +
                          "Thread title: " + str(x.title) + "\n" +
                          "Total comments: " + str(len(comments)) + "\n" +
                          "Total downvotes: " + str(self.downvotes))
                
                self.r.send_message(self.boss, 'DVFB found downvoted thread', message)


    def reset(self):
        self.sub_name = ""
        self.sub = 0
        self.sub_threads = 0

    #possible subs that bot can choose.
    def init_stuff(self):

        #counts the total times run
        self.counter = 0

        self.limit = 10
        self.login_name = ""
        self.login_pass = ""
        self.boss = "" #this is user that gets messages and reports sent to.
        
        self.possible_subs = []
        self.possible_subs.append('askreddit')
        self.possible_subs.append('nba')
        self.possible_subs.append('starcraft')
        self.possible_subs.append('random')
        self.possible_subs.append('random')
        self.possible_subs.append('random')
        self.possible_subs.append('random')
        self.possible_subs.append('random')
        self.possible_subs.append('random')
        self.possible_subs.append('random')
        self.possible_subs.append('random')
        self.possible_subs.append('random')
        self.possible_subs.append('random')




def main():
    bot = RedditBot()

    bot.init_stuff()
    bot.login()

    while(True):

        try:
            bot.run()
        except:
            bot.r.send_message(bot.boss,'ERROR MESSAGE', "something went wrong.")
            pass

        #sleep for 5 minutes.
        print("Found: " + str(bot.downvotes) + " bad threads.")
        time.sleep(10)

        bot.reset()
        
    



if __name__ == '__main__':
    main()
