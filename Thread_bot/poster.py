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

        
        home_team = fetch_object.home_starters_stats
        road_team = fetch_object.road_starters_stats

        subreddit = self.config.get('reddit_stuff', 'target_subreddit')

        
        title = "Pre - Game Thread" + str(game['road_team']) + " at " + str(game['home_team']+ "( " + str(fetch_object.print_date) + " ):  " )

        #####################################################################################
        #>>>>>>>>>>>>>>>>>>>>>THERE HAS TO BE A BETTER WAY. FIND IT XENG. FIIINNNNND IT.<<<<<<<<<<<<<<<<<<<<<<<<<
        ###################################################################################
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



|||||||**%s**|||||||
:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:
**Name**|**GP**|**GS**|**MIN**|**PPG**|**OFFR**|**DEFR**|**RPG**|**APG**|**SPG**|**BPG**|**TPG**|**FPG**|**A/TO**|**PER**
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s

>

|||||||**%s**|||||||
:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:
**Name**|**GP**|**GS**|**MIN**|**PPG**|**OFFR**|**DEFR**|**RPG**|**APG**|**SPG**|**BPG**|**TPG**|**FPG**|**A/TO**|**PER**
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s
**%s**|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s




""" % (game['road_team'], game['road_team_link'],(str(game['preview_link'])), game['home_team'], game['home_team_link'],
        game['tickets'], game['tickets_link'], game['away_tv'], game['home_tv'],

       game['home_team'],
       home_team[0].dictionary['name'], home_team[0].dictionary['gp'], home_team[0].dictionary['gs'],home_team[0].dictionary['min'],
       home_team[0].dictionary['ppg'],home_team[0].dictionary['offr'],home_team[0].dictionary['defr'],home_team[0].dictionary['rpg'],
       home_team[0].dictionary['apg'],home_team[0].dictionary['spg'],home_team[0].dictionary['bpg'],home_team[0].dictionary['tpg'],
       home_team[0].dictionary['fpg'],home_team[0].dictionary['ato'],home_team[0].dictionary['per'],

       home_team[1].dictionary['name'], home_team[1].dictionary['gp'], home_team[1].dictionary['gs'],home_team[1].dictionary['min'],
       home_team[1].dictionary['ppg'],home_team[1].dictionary['offr'],home_team[1].dictionary['defr'],home_team[1].dictionary['rpg'],
       home_team[1].dictionary['apg'],home_team[1].dictionary['spg'],home_team[1].dictionary['bpg'],home_team[1].dictionary['tpg'],
       home_team[1].dictionary['fpg'],home_team[1].dictionary['ato'],home_team[1].dictionary['per'],

       home_team[2].dictionary['name'], home_team[2].dictionary['gp'], home_team[2].dictionary['gs'],home_team[2].dictionary['min'],
       home_team[2].dictionary['ppg'],home_team[2].dictionary['offr'],home_team[2].dictionary['defr'],home_team[2].dictionary['rpg'],
       home_team[2].dictionary['apg'],home_team[2].dictionary['spg'],home_team[2].dictionary['bpg'],home_team[2].dictionary['tpg'],
       home_team[2].dictionary['fpg'],home_team[2].dictionary['ato'],home_team[2].dictionary['per'],

       home_team[3].dictionary['name'], home_team[3].dictionary['gp'], home_team[3].dictionary['gs'],home_team[3].dictionary['min'],
       home_team[3].dictionary['ppg'],home_team[3].dictionary['offr'],home_team[3].dictionary['defr'],home_team[3].dictionary['rpg'],
       home_team[3].dictionary['apg'],home_team[3].dictionary['spg'],home_team[3].dictionary['bpg'],home_team[3].dictionary['tpg'],
       home_team[3].dictionary['fpg'],home_team[3].dictionary['ato'],home_team[3].dictionary['per'],

       home_team[4].dictionary['name'], home_team[4].dictionary['gp'], home_team[4].dictionary['gs'],home_team[4].dictionary['min'],
       home_team[4].dictionary['ppg'],home_team[4].dictionary['offr'],home_team[4].dictionary['defr'],home_team[4].dictionary['rpg'],
       home_team[4].dictionary['apg'],home_team[4].dictionary['spg'],home_team[4].dictionary['bpg'],home_team[4].dictionary['tpg'],
       home_team[4].dictionary['fpg'],home_team[4].dictionary['ato'],home_team[4].dictionary['per'],

       game['road_team'],
       road_team[0].dictionary['name'], road_team[0].dictionary['gp'], road_team[0].dictionary['gs'],road_team[0].dictionary['min'],
       road_team[0].dictionary['ppg'],road_team[0].dictionary['offr'],road_team[0].dictionary['defr'],road_team[0].dictionary['rpg'],
       road_team[0].dictionary['apg'],road_team[0].dictionary['spg'],road_team[0].dictionary['bpg'],road_team[0].dictionary['tpg'],
       road_team[0].dictionary['fpg'],road_team[0].dictionary['ato'],road_team[0].dictionary['per'],

       road_team[1].dictionary['name'], road_team[1].dictionary['gp'], road_team[1].dictionary['gs'],road_team[1].dictionary['min'],
       road_team[1].dictionary['ppg'],road_team[1].dictionary['offr'],road_team[1].dictionary['defr'],road_team[1].dictionary['rpg'],
       road_team[1].dictionary['apg'],road_team[1].dictionary['spg'],road_team[1].dictionary['bpg'],road_team[1].dictionary['tpg'],
       road_team[1].dictionary['fpg'],road_team[1].dictionary['ato'],road_team[1].dictionary['per'],

       road_team[2].dictionary['name'], road_team[2].dictionary['gp'], road_team[2].dictionary['gs'],road_team[2].dictionary['min'],
       road_team[2].dictionary['ppg'],road_team[2].dictionary['offr'],road_team[2].dictionary['defr'],road_team[2].dictionary['rpg'],
       road_team[2].dictionary['apg'],road_team[2].dictionary['spg'],road_team[2].dictionary['bpg'],road_team[2].dictionary['tpg'],
       road_team[2].dictionary['fpg'],road_team[2].dictionary['ato'],road_team[2].dictionary['per'],

       road_team[3].dictionary['name'], road_team[3].dictionary['gp'], road_team[3].dictionary['gs'],road_team[3].dictionary['min'],
       road_team[3].dictionary['ppg'],road_team[3].dictionary['offr'],road_team[3].dictionary['defr'],road_team[3].dictionary['rpg'],
       road_team[3].dictionary['apg'],road_team[3].dictionary['spg'],road_team[3].dictionary['bpg'],road_team[3].dictionary['tpg'],
       road_team[3].dictionary['fpg'],road_team[3].dictionary['ato'],road_team[3].dictionary['per'],

       road_team[4].dictionary['name'], road_team[4].dictionary['gp'], road_team[4].dictionary['gs'],road_team[4].dictionary['min'],
       road_team[4].dictionary['ppg'],road_team[4].dictionary['offr'],road_team[4].dictionary['defr'],road_team[4].dictionary['rpg'],
       road_team[4].dictionary['apg'],road_team[4].dictionary['spg'],road_team[4].dictionary['bpg'],road_team[4].dictionary['tpg'],
       road_team[4].dictionary['fpg'],road_team[4].dictionary['ato'],road_team[4].dictionary['per'],
            )

        
        self.r.submit(subreddit, title, message).sticky()
        print("THREAD POSTED GO CHECK!")
        


    def post_game(self, fetch_object):
        dd = 3

    def post_postgame(self, fetch_object):
        dd = 4


    



