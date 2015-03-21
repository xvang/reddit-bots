import praw
import os
import time

from poster import Poster
from fetcher import Fetcher
from database import Database

import warnings
class Thread:

    def __init__(self):

        self.postManager = Poster()
        self.fetchManager = Fetcher()

        self.posted_pre = False
        self.posted_game = False
        self.posted_post = False


    def run(self):

        #If game info has not been fetched, then get the info.
        #Once the info is fetched, the "fetched" boolean will become true.

        #TODO: undo the stuff here.
        if ( not self.fetchManager.fetched_pregame ):
            self.fetchManager.fetch_pre_game_info()
            #self.fetchManager.fetch_post_game_info()


        
        #Check if there is a game today. "game_day" is a boolean.
        game_day = self.fetchManager.is_gameday_today()

        if (game_day):
            
            #Get the game time and the current time.
            #game_time = self.fetchManager.get_game_time()
            #current_time = self.fetchManager.get_current_time()
            game_time = 2
            current_time = 20

            #print("Time difference: " + str(game_time - current_time))


            #time_left = game_time - current_time

            #for testing purposes we manually input into 'time_left'
            #XENG DELETE LATER!!!@!@!@!!!@!@!@@!
            time_left = 500
            #If 5 minutes before tipoff, then post the game thread.
            if (not self.posted_game and time_left <= 300):
               # self.postManager.post_game( self.fetchManager )
                self.posted_game = True
                
                
            
            #if 30 minutes before tipoff, then post the pre-game thread.
            elif (not self.posted_pre and time_left <= 1800):            
                self.postManager.post_pregame( self.fetchManager )
                self.posted_pre = True

            #Average game is 2:30
            #So 2 hours and 30 minutes after game thread,
            #the post-game thread is posted.
            elif (not self.posted_post and time_left <= -9000):
                self.postManager.post_postgame( self.fetchManager )
                self.posted_post = True

                




def main():

    thread = Thread()


    while(True):
        thread.run()

        print("Finished a run!")
        time.sleep(1200)
    
    

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    main()
