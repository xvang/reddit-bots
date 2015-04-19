import praw
import configparser
import time
from matlib import MatLib
import warnings
def get_favorite_words(redditor, all_all, check_comments):

    words = {}

    #Not sure how line below works at the moment, the syntax is confusing
    #http://stackoverflow.com/questions/2171095/python-efficient-method-to-remove-all-non-letters-and-replace-them-with-unders
    #it removes all non-letter and non-numbers from the user's comments.
    removed = "".join(chr(c) if chr(c).isupper() or chr(c).islower() or chr(c).isdigit() or (chr(c) == "'") else " " for c in range(256))

    for thing in all_all:
        comment_array = None

        #If 'check_comments' == True, then we are counting words in comment.
        #If 'check_comments' == False, then we are counting words in submission title.
        if(check_comments):
            comment_array = thing.body.lower().translate(removed).split()
        else:
            comment_array = thing.title.lower().translate(removed).split()
        for word in comment_array:
            try:
                words[word] = int(words[word]) + 1
            except:
                words[word] = 1

    #'what' is a list(?) that contains tuples that hold a key and value.
    #'what' is now in order by value. Smallest to largest
    what = sorted(words.items(), key=lambda x: x[1])

    if(len(what) > 10):
        what = what[-11:-1]

   # if(check_comments):
    #    print("CHECKING COMMENTS")
   # else:
  #      print("CHECKING TITLES")
 #   for w in what:
  #      print(w[0], ": ", w[1])

    #Returns the 10 most used words, and how many times each word is used.
    return what

def get_comment_age(comments):
    age = []
    for comment in comments:
        age.append(comment.created_utc)

    return age
    
#Fetch a breakdown of a user's karma by subreddit.
def get_karma_by_subreddit(all_submissions, all_comments):

    link_karma_count = {}
    comment_karma_count = {}

    for thing in all_submissions:
        subreddit = thing.subreddit.display_name
        link_karma_count[subreddit] = (link_karma_count.get(subreddit, 0) + thing.score)

    #now we get all the comments made by the user.
    
    for c in all_comments:
        subreddit = c.subreddit.display_name
        comment_karma_count[subreddit] = (comment_karma_count.get(subreddit, 0) + c.score)

    #I wanted fetching karma by subreddit to be in its own function( apart from gather_info() )
    #and I wanted link karma and comment karma to be separated
    #but I didn't want a function for fetching link karma, and one for fetching comment karma.
    #So I retrieved them separately here, and return them together in a dict.
    all_karma = {}
    all_karma['link'] = link_karma_count
    all_karma['comment'] = comment_karma_count
    
    return all_karma
    

def gather_info(r, user, message):

    redditor = None
    try:
        redditor = r.get_redditor(user)
    except:
        message.reply("tmi-bot says: \n\n" + "/u/"+user + " does not exist.")
        return #Error message is sent. No need to go further.

    #'info' stores all the info about the user.
    info = {}

    #Apparently, the two things below are 'generator' objects
    #And they can only be iterated ONCE
    #So we iterate through them and store the 'comment' objects in a list
    submission_gen = redditor.get_submitted(limit=None)
    comment_gen = redditor.get_comments(sort='top', time='all', limit=None)

    all_submissions = []
    all_comments = []

    for x in submission_gen:
        all_submissions.append(x)

    for x in comment_gen:
        all_comments.append(x)

    

    #get the breakdown of karma by subreddit.
    all_karma = get_karma_by_subreddit(all_submissions=all_submissions, all_comments=all_comments)
    info['link_karma_by_subreddit'] = all_karma['link']
    info['comment_karma_by_subreddit'] = all_karma['comment']

    
    #done
    info['link_karma'] = int(redditor.link_karma)

    #done
    info['comment_karma'] = int(redditor.comment_karma)

    info['favorite_words_comment'] = get_favorite_words(redditor=redditor, all_all=all_comments, check_comments=True)
    info['favorite_words_title'] = get_favorite_words(redditor=redditor, all_all=all_submissions, check_comments=False)

    info['comment_ages'] = get_comment_age(comments = all_comments)

    


    #print(info)
    matlib = MatLib(info=info)

    

def check_mail(r):

    unread = r.get_unread(limit=None)


    for message in unread:
        if("graph" in message.body.lower()):
            user = message.body.lower().split()[1]

            print("USER: ", user)

            #In case the message had a "/u/", we remove it. We don't want those.
            gather_info(r=r, user=str(user).strip('/u/'), message=message)
            #message.mark_as_read()
    




if __name__=="__main__":

    r = praw.Reddit("/u/habnpam too much info with charts.")
    warnings.filterwarnings("ignore")
    config = configparser.ConfigParser()
    config.read('authoriteh.ini')
    
    r.login(config.get('reddit_stuff', 'username'),config.get('reddit_stuff', 'pass'))

    counter = 0
    while(True):


        check_mail(r=r)

        counter = counter + 1
        print("Counter: ", counter)
        time.sleep(3333330)
