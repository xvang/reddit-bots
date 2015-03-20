import praw
import urllib
import time
import imgurpython
from imgurpython import ImgurClient
import configparser

import urllib.request



def post_to_imgur(picture, _bot):

    # "login" to Imgur with credentials.
    config = configparser.ConfigParser()
    config.read('auth.ini')
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')
    access_token = config.get('credentials', 'access_token')
    refresh_token = config.get('credentials', 'refresh_token')
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)

    configure = {
        'album': None,
        'name': 'Name Here',
        'title': 'Title goes here',
        'description': 'description goes here',
                 }
    
    image = client.upload_from_path(picture, config=configure, anon=False)


    return image['link']


def post_to_reddit( _bot, link, submission):

    m = "Your picture is not from Imgur, or it was from mobile Imgur. \n"
    e = "[It has been rehosted on Imgur.](%s)" % link
    s = " \n \n ---  \n \n"
    a = "^^^I ^^^am ^^^rehost ^^^bot."

    message = m  + e + s + a

    #submission.add_comment(message)
    _bot.send_message("habnpam", "FFFFFFFFF", message)
    print("Message posted to Reddit")


    
def parse_subreddit(bot):

    #Getting the desired subreddit to check.
    subreddit = bot.get_subreddit("offensive_wallpapers")

    #Getting the 5 newest posts.
    new_posts = subreddit.get_new(limit=5)

    #these are the words that we will test for.
    mobile_imgur = "m.imgur.com"
    imgur = "imgur.com"

    

    #store the ID's of previously check submissions into a list.
    already_done = []

    #stores the ID of new comments. These will be added to history.txt later.
    new_comments = []

    #open the file containing previously checked submissions.
    file  = open("history.txt", "r")
    
    for x in file:
        already_done.append(x.rstrip('\n'))

    file.close()

    counter = 0
    for x in new_posts:
        counter = counter + 1
        #get the URL that the post links to.
        url = str(x.url)
        
        #(If link was to mobile Imgur, or did not link to Imgur ) and (link has not been checked).
        #We download the picture.
        if (( mobile_imgur in url) or ( imgur not in url) ) and (x.id not in already_done):
            d=  4
            print("New Comment")

'''
            try:
                
                name = str(counter) + ".jpg"
                print(name)
                urllib.request.retrieve(url, name)
                
                #new_link will store the URL of the newly posted image on Imgur
                new_link = post_to_imgur(picture = name, _bot = bot)

                #posts the link in the comment section of the post.
                post_to_reddit(_bot=bot, link  = new_link, submission=x)

                new_comments.append(x.id)
            except:
                print("Could not access picture.")             
                pass'''
            


    #Now that we have gone through the new comments,
    #We add the ID of them into history.txt so we don't check them multiple times.
    write  = open("history.txt", "a")
    
    for x in new_comments:
        write.write(str(x) + "\n")

    write.close()

    print("Number of new comments: " + str(counter))

    #Remove the pictures that were saved.
    remove_pictures(counter)

def remove_pictures(counter):

    while counter > 0:
        try:
            os.remove(str(x) + ".jpg")
        except:
            print("could not remove picture!")
            pass
        counter = counter - 1
###################
##              MAIN             ##
###################


config = configparser.ConfigParser()
config.read('auth.ini')
username = config.get('reddit_stuff', 'username')
password = config.get('reddit_stuff', 'password')
target_subreddit = config.get('reddit_stuff', 'target_subreddit')
bot_name = config.get('reddit_stuff', 'bot_name')


r = praw.Reddit(user_agent=bot_name)
r.login(username, password)


while(True):

    parse_subreddit(bot = r)


    print("Finished  a run.")
    gg = input("pausepausepause")

    
    time.sleep(120)
    #pause the bot for 120 seconds, or however long you want.
    #But it should be at least 60, to be safe.

    



