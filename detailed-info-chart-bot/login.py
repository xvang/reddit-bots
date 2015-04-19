import praw
import configparser


if __name__=="__main__":

    config = configparser.ConfigParser()
    config.read('authoriteh.ini')


    r = praw.Reddit(user_agent=config.get('reddit_stuff', 'botname'))

    r.set_oauth_app_info(client_id=config.get('reddit_stuff', 'clientid'),
                         client_secret=config.get('reddit_stuff', 'clientsecret'),
                         redirect_uri=config.get('reddit_stuff', 'redirect_uri'))
    
    # the function will return a new 'access_token'             
    refreshed = r.refresh_access_information(config.get('reddit_stuff', 'refresh_token'))
    
    #"log in" with the credentials.
    r.set_access_credentials(access_token=refreshed['access_token'],
                             refresh_token=refreshed['refresh_token'],
                             scope=refreshed['scope'])

    print("HELLOOOO")


'''
#Every hour, get new access token.hour=3600 seconds, but 2900 is there to be safe.
            if(time.time() - time_refreshed > 2900):
                # the function will return a new 'access_token'             
                refreshed = r.refresh_access_information(os.environ['refresh_token'])
    
                #"log in" with the credentials.
                r.set_access_credentials(access_token=refreshed['access_token'],
                refresh_token=refreshed['refresh_token'],
                scope=refreshed['scope'])
                    
                #update the refreshed time.
                time_refreshed = time.time()

'''
