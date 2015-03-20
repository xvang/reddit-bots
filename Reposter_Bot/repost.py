import praw
import time

'''
Uses Reddit API(praw) to get certain submissions
from certain subreddits and reposts.
'''
class RedditBot():

    def __init__(self, parent=None):
        super(RedditBot, self).__init__()


#=================================================================#
#================= CHANGE THE STUFF BELOW ========================#
#=================================================================#
        self.login_name = ""                                #username
        self.login_pass = ""                              #password
        self.bot_name= "archive_reposting_bot_3909"                 #name for the bot

        self.repost_comments = True                                 #toggle whether or not to repost the comments. True = yes. False = no.

        self.time_limit = 180                                       #In days, how far back you want to search.


        self.check_these_subs = ["",
                                 ]                                  #list of subreddits where you want to get the archived stuff from.
        
        self.sub_to = ""                                    #subreddit where you want to repost the archived stuff to
        

        self.repost_limit = 100                                     #Limits the amount of archived post the bot will repost.
                                                                    #Some subs might have thousands of archived stuff.
                                                                    #Or if you don't care, set it to a 1000
                                                                    #to repost up to the maximum 1000.
                                                                    #But that will take a while to complete.
        
#=================================================================#
#================= CHANGE THE STUFF ABOVE ========================#
#=================================================================#



    def user_init(self):

        #connecting to Reddit.
        self.r = praw.Reddit(user_agent = self.bot_name)

        #logging in.
        self.r.login(self.login_name, self.login_pass)

        #stores id of posts to be reposted.
        self.id_storage = []
       
        

    #gathers the posts. (only up to 1000)
    def gather_post_ID(self, target_sub):
        print("Checking sub: " + target_sub)
        #getting desired subreddit.
        sub = self.r.get_subreddit(target_sub).get_top_from_all(limit=None)


        current_time = int(time.time())

        #stores the list of post older than 6 months that have already been reposted.
        file = open("history.txt", 'r')

        #stores the id's in a list.
        history = []
        for f in file:
            history.append(f.rstrip('\n'))
        file.close()
        
        #iterate through the posts.
        for post in sub:

            #(current_time - posted_time)
            post_age = (current_time - post.created_utc) / 60/ 60 / 24

            #if post is older than 6 months.
            if(post_age >= self.time_limit):

                #if post has not been stored in id_storage list yet, and repost limit has not been reached.
                if post.id not in history and len(self.id_storage) <= self.repost_limit:
                    self.id_storage.append(post.id)

            
    def time_to_repost(self):
        print("time to repost")
        #stores the post_id in history.txt so the next time we don't repost the same archived post.
        out = open("history.txt", 'a')
        #retrieves each post one at a time and gathers all the necessary info about them to repost.
        for post_id in self.id_storage:

            #write out to file.
            out.write(str(post_id) + "\n")

            #retrieve the post using the id
            post = self.r.get_submission(submission_id = str(post_id))


            #gets the text in the post.
            _post_text = post.selftext

            #get the url that the post directs to.
            _url = post.url

            #gets the title of the post
            _title=post.title

            #stores all the top level comments from the post.
            _comment_storage = []
            
            for comments in post.comments:
                try:
                    _comment_storage.append(str(comments.body))
                except:
                    print("could not get comments. Probably just 1 and it was deleted...?")
                    pass

            try:
                #repost is done here.
                _new_post = self.r.submit(self.sub_to, title=_title, url=_url ,resubmit=True)
                #passes the post object to different function to add the top level comments.            
                self.add_the_comments(new_post_id=_new_post.id, comment_storage=_comment_storage)
            except:
                print("could not submit a certain post. URL is probably banned or does not exist.")
                print("Or the reddit account is new and must wait a bit.")
                pass

        out.close()
        self.id_storage[:] = []

    #Adding comments.
    def add_the_comments(self, new_post_id, comment_storage):


        if(self.repost_comments):
            #retrieves the new post.
            post = self.r.get_submission(submission_id=new_post_id)

            for comment in comment_storage:
                
                #terrible way of checking if a comment has links. links are made like this: [words](url) so I check for the brackets.
                #but it should work. thats what counts. right? right?
                #I also checked for parentheses because [deleted] has brackets.
                if( "[" in comment and "]" in comment and "(" in comment and ")" in comment):
                    try:
                        post.add_comment(comment)
                    except:
                        print("unable to add comment. Probably because the account is new?")
                        pass
                    


def main():

    bot = RedditBot()

    bot.user_init()


    for subs in bot.check_these_subs:
        
        bot.gather_post_ID(subs)
        bot.time_to_repost()


    print("Finished.")



if __name__ == '__main__':
    main()
