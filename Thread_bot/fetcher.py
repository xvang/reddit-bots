import praw
import os
import time
import urllib
from bs4 import BeautifulSoup
import datetime

from player import Player


class Fetcher:

    def __init__(self):
        s = 3

        self.team = "Chicago"                                  #Team to post for.
        self.fetched_pregame = False                        #if true, then already fetched game info.
        self.date_list = None                                   #["weekday", "month", "date"]
        self.weekday = 0                                         #0 = Monday, 1 = Tuesday, etc.
        self.pre_game  = {}                                     #dictionary that contains most of the game information.
        self.post_game = {}

        self.home_team_list = []                                #stores a list of players and their stats.
        self.road_team_list = []                                  #stores a list of players and their stats.

        self.home_starters = []                                  #stores a list of the starters for the home team
        self.road_starters = []                                   #stores a list of the starters for the road team

        self.home_starters_stats = []                           #redundant?
        self.road_starters_stats = []
        self.game_today = False
        self.weekday_conversion = {'Monday': 0,
                                   'Tuesday':1,
                                   'Wednesday': 2,
                                   'Thursday': 3,
                                   'Friday': 4,
                                   'Saturday': 5,
                                   'Sunday': 6}

        self.month_conversion = {'January':1,
                                 'February':2,
                                 'March': 3,
                                 'April': 4,
                                 'May': 5,
                                 'June': 6,
                                 'July': 7,
                                 'August': 8,
                                 'September': 9,
                                 'October': 10,
                                 'November': 11,
                                 'December': 12}

        self.url_team_conversion = {'Atlanta': 'atl',
                                    'Boston':'bos',
                                    'Brooklyn':'bkn',
                                    'Charlotte':'cha',
                                    'Chicago':'chi',
                                    'Cleveland':'cle','Dallas':'dal',
                                    'Denver':'den','Detroit':'det',
                                    'Golden State':'gsw','Houston':'hou',
                                    'Indiana':'ind','LA Clippers':'lac',
                                    'LA Lakers':'lal','Memphis':'mem',
                                    'Miami':'mia','Milwaukee':'mil',
                                    'Minnesota':'min','New Orleans':'no',
                                    'New York':'ny','Oklahoma City':'okc',
                                    'Orlando':'orl','Philadelphia':'phi',
                                    'Phoenix':'pho','Portland':'por',
                                    'Sacramento':'sac','San Antonio':'sas',
                                    'Toronto':'tor','Utah':'utah',
                                    'Washington':'was'}
    
    def is_gameday_today(self):
        return True
        #return self.game_today


    #Fetch information about the game from [ espn.com ] .
    def fetch_pre_game_info(self):

        url = "http://scores.espn.go.com/nba/schedule"
        page  = urllib.request.urlopen(url)

        soup = BeautifulSoup(page)

        #get the schedule for the week.
        div = soup.find('div', {'class':'mod-container mod-table mod-no-header-footer'})


        #get all the games (for the week, I think) that is displayed.
        table = div.find_all('table', {'class':'tablehead'})

        target_table = table[0]

        #if the games are played already, then the first table will be the results.
        #We don't want results from here. We want the upcoming games.
        #The next games should be in the second table.
        #It's late and I'm still working on this, and the page changed to show results, so I had to change with it. 
        #We should NEVER have to check the second table. This webpage should only be parsed for pre-game stuff.
        if("result" in table[0].text.lower()):
            target_table = table[1]



        #The 'stathead' class contains the date.
        game_date = target_table.find('tr', {'class':'stathead'})

        #convert the date into a list. ["weekday", "month", "date"]
        game_date = str(game_date.text).replace(",", " ").split()

        #convert the "weekday" string into numbers.
        game_date[0] = self.weekday_conversion[game_date[0]]

        #convert the "month" string into numbers.
        game_date[1] = self.month_conversion[game_date[1]]

        #convert the "day" string into numbers.
        game_date[2] = int(game_date[2])

        #stores the list into 'date_list'
        #maybe we should have worked with this variable instead?
        self.date_list = game_date.copy()

        #Now that we have the date, we check if the team is playing.
        #'table' contains all of today's games.
        tr = target_table.find_all('tr',{})

        #each game info is stored in a 'tr'
        for x in tr:

            #If team is playing, then its name will be in the text.
            if (self.team in x.text):
                
                self.game_today = True
                
                x_list = list(x)


                teams = x_list[0].text.split() #["team1", "at", "team2"]

                self.pre_game['road_team'] = teams[0]
                self.pre_game['home_team'] = teams[2]
                self.pre_game['teams'] = x_list[0].text
                self.pre_game['time'] = x_list[1].text
                self.pre_game['away_tv'] = x_list[3].text
                self.pre_game['home_tv'] = x_list[4].text
                self.pre_game['tickets'] = x_list[6].text

                
                #get all the links.
                a_all = x.find_all('a', href=True)

                #Some games have the "Watch on ESPN" link, and some don't.
                #So to solve that problem, all those are excluded.
                self.pre_game['road_team_link'] = a_all[0]['href']
                self.pre_game['home_team_link'] = a_all[1]['href']
                self.pre_game['preview_link'] = str(a_all[2]['href'])
                self.pre_game['tickets_link'] = a_all[-1]['href']

                #found team, no need to check further.
                break


        #Fetch all the player on the roster's stats.
        self.fetch_player_stats(self.url_team_conversion[self.pre_game['home_team']], self.home_team_list)
        self.fetch_player_stats(self.url_team_conversion[self.pre_game['road_team']], self.road_team_list)

        #Fetch the starters.
        self.fetch_starters(self.url_team_conversion[self.pre_game['home_team']],self.home_starters)
        self.fetch_starters(self.url_team_conversion[self.pre_game['road_team']], self.road_starters)


        #Fetching the starters' stats from the team lists and storing them into a different list.
        #Redundant, but it's easier to sort them this way. I think.
        for x in self.home_starters:
            for y in self.home_team_list:
                if(str(x) in y.dictionary['name']):
                    self.home_starters_stats.append(y)
                    break;


        for x in self.road_starters:
            for y in self.road_team_list:
                if (str(x) in y.dictionary['name']):
                    self.road_starters_stats.append(y)
                    break;


        


        #At the very end of fetch_game_info(), we toggle "fetched" to true.
        #If something went wrong while parsing, then this statement should never be executed.
        self.fetched_pregame = True

    def fetch_starters(self, team_name, team_list):
        url = "http://espn.go.com/nba/team/depth/_/name/"  + team_name

        page = urllib.request.urlopen(url)

        soup = BeautifulSoup(page)

        div = soup.find('div', {'class': 'mod-container mod-table'})

        #The div above contains 2 elements: another div with all the players stats,
        #and a link to "full depth charts". We want just the first one.
        table = div.find('table',{})

        for tr in table:
            counter = 0
            for names in tr:
                if((counter == 1) and (not names.text.lower() == "starter")):
                    team_list.append(names.text)
                    break;                                  #we break because we only want the first column, which are the starters.
                counter = counter + 1               #Using a counter here is a temporary solution. We only want the [1] element of each row.
        
    #Fetch starting players.
    def fetch_player_stats(self, team_name, team_list):
        url = "http://espn.go.com/nba/team/stats/_/name/" + team_name

        page = urllib.request.urlopen(url)

        soup = BeautifulSoup(page)

        #The parsing strategy is as such:
        #Get the 'div' that holds all the stats. In that 'div' is just the one table with all the stats.
        #In that table are 'tr' which are the rows.
        #In each 'tr' are each individual numbers, which are stored as text in 'td'.
        div = soup.find('div', {'class':'mod-container mod-table'})

        table  = div.find('table',{})
        

        #the find() method returns the FIRST tag that qualifies.
        #the find_all() method returns ALL tags that qualify.
        #Here we want all the 'tr' or rows in the table.
        tr = table.find_all('tr',{})


        #Each 'tr' has a bunch of 'td' tags in them. Those are the ones that have the numbers.
        for td in tr:
            player = Player()

            for link in td.find_all('a', href=True):
                player.input_link(link['href'])
                break;
            
            for x in td:

                #The if-statement prevents adding the first 2 rows as a "players". They are headers.
                if(x.text.lower() in "game statistics" or x.text.lower() in "player"):
                    break;
                
                player.brute_input(x.text)

                
            #if-statement is exclude the first two rows.
            if((not player.dictionary['name'] == "name" ) and (not str(player.dictionary['name']).lower() == "totals")):
                team_list.append(player)

                
            
            
            


#################################################################################
#################################################################################            
    def fetch_post_game_info(self):
        url = "http://espn.go.com/nba/schedule"
        page  = urllib.request.urlopen(url)

        soup = BeautifulSoup(page)


    def get_live_game_info(self):
        url = "https://espn.go.com/nba/schedule"




    #The time is in the form XX:XX AM/PM
    #We want to get it into UTC form like this: 4230948720938123
    def get_game_time(self):

        time_list = self.pre_game['time'].replace(":", " ").split()

        time_list[0] = int(time_list[0])
        time_list[1] = int(time_list[1])

        #convert to 24 hours time.
        if time_list[2] == "PM" and time_list[0] < 12:
            time_list[0] = time_list[0] + 12

        year = datetime.date.today().year
        month = self.date_list[1]
        day = self.date_list[2]

        hour = time_list[0]
        minute = time_list[1]

        dt = datetime.datetime(year, month, day, hour, minute)
        time_in_seconds = time.mktime(dt.timetuple())

        #print("Game Time: " + str(time_in_seconds))
        return time_in_seconds



    def get_current_time(self):
        #print("Current Time: " + str(time.time()))
        return time.time()

    
        