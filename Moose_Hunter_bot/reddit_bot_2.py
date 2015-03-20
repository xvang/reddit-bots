import praw
import time
import os


class RedditBot():

    def __init__(self, parent=None):
        super(RedditBot, self).__init__()
        self.Init()
        self.runBot()


    def Custom_Init_Variables(self):
        
        ########################################################
        ################   Change Stuff Here!   ################
        ##   Read the README.txt file for more information!   ##
        ########################################################
        
        self.message = "Hello from Moose_Hunter_Bot!"

        self.RUN_FOREVER = False

        self.period = 630

        self.target_User = "-moose-"

        self.pause = 1
        
        self.login_name = 'Moose_Hunter_Bot'
        self.login_password = 'queequeger'
        
        self.bot_name = 'moose_hunter_for_queequeger'
        


    def runBot(self):

        while(self.loop):
            self.Open_Commented_History()
        
            self.Retrieve_New_Comments()

            self.Update_Commented_History()

            self.Reply()

            #If only running once, then self.loop will become false here.
            self.loop = self.RUN_FOREVER

            #pause for however long before re-iterating.
            time.sleep(self.period)

            self.ClearVariables()

    #Logging in to Reddit.
    def Init(self):

        self.message = "Hello from Moose_Hunter_Bot!"
        self.RUN_FOREVER = False
        self.loop = True
        self.period = 630
        self.target_User = ""
        self.pause = 630

        self.login_name = 'Moose_Hunter_Bot'
        self.login_password = 'queequeger'
        self.bot_name = 'moose_hunter_for_queequeger'
        
        self.Custom_Init_Variables()

        #Stores the most recent 10 comments separately.
        self.comments = []
        self.recent_commentID = []

        #these are the comments the bot will respond to.
        self.todo_Comment = []
        
        self.history = []

        
        self.r = praw.Reddit(user_agent=self.bot_name)
        self.r.login(self.login_name, self.login_password)#username, password
        
        self.user = self.r.get_redditor(self.target_User)

    #Retrieves 10 most recent comments that the user made.
    def Retrieve_New_Comments(self):

        for c in self.user.get_comments(limit=10):
            self.comments.append(c)
            self.recent_commentID.append(c.id)



    #Loads in comments that bot has already responded to.
    def Open_Commented_History(self):
        
        if( not self.r.is_logged_in()):
            self.InitLogin()
        try:
            history_file = open("history.txt")
            for h in history_file:
                self.history.append(h.rstrip('\n'))
			history_file.close()
        
        except FileNotFoundError:
            os._exit(1) #This might be a no-no. It works, but there's probably a better way to exit.
                        #What I'm trying to do is completely exit the program if there is no
                        #file name history.txt in the same directory. It should never be get
                        #to that case anyways.  It's just here for the sake of things.


    #Checks whether or not a comment has been responded to.
    #If not, then it adds the comment ID to the comment history txt file.
    def Update_Commented_History(self):

        #checking for comments that have not been responded to.
        for x in self.recent_commentID:
            if not x in self.history:
                self.todo_Comment.append(x)

        #Adding the new comments into the comment history.
        out = open("history.txt", 'a')
        for x in self.todo_Comment:
            out.write(str(x) + "\n")
        out.close()

    def Reply(self):

        for x in self.todo_Comment:
            for y in self.comments:
                if(x == y.id):
                    y.reply(self.message)
                    time.sleep(self.pause)
                    break



    #clears the variables
    def ClearVariables():
        self.comments[:] = []
        self.recent_commentID[:] = []
        self.history[:] = []
        self.todo_Comment[:] = []
        

def main():
    bot = RedditBot()
    



if __name__ == '__main__':
    main()
