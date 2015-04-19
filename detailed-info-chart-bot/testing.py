import praw
import configparser


if __name__=="__main__":

    config = configparser.ConfigParser()
    config.read('authoriteh.ini')


    r = praw.Reddit(user_agent=config.get('reddit_stuff', 'botname'))

    r.login(config.get('reddit_stuff','username'), config.get('reddit_stuff', 'pass'))
    
    print("HELLOOOO")

