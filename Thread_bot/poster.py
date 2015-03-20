import praw
import os
import time
import configparser


#TODO: implement OAuth??? But its so stupid difficult.
class Poster:

    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('authoriteh.ini')
        name = self.config.get('reddit_stuff', 'name')
        password = self.config.get('reddit_stuff', 'password')
        botname = self.config.get('reddit_stuff', 'botname')
        self.r = praw.Reddit(user_agent=botname)
        self.r.login(name, password)


    def post_pregame(self, fetch_object):

        #'fetch_object' contains all the info about the game.
        game = fetch_object.pre_game


        subreddit = self.config.get('reddit_stuff', 'target_subreddit')

        title = "PreGame Thread: " + str(game['teams'])


        message = """###Coming in live from somewhere over there. Not here.

---

Road Team|Info|Home Team
:-:|:-:|:-:
[%s](%s)| [ESPN Preview](%s) | [%s](%s)


OVERVIEW|.
:-:|:-:
Ticket Information | [%s](%s)
TV Information | Road Team: %s , Home Team: %s


>


>



""" % (game['road_team'], game['road_team_link'],(str(game['preview_link'])), game['home_team'], game['home_team_link'],
        game['tickets'], game['tickets_link'], game['away_tv'], game['home_tv'],
            )

        
        self.r.submit(subreddit, title, message).sticky()
        print("THREAD POSTED GO CHECK!")
        


    def post_game(self, fetch_object):
        dd = 3

    def post_postgame(self, fetch_object):
        dd = 4


    



