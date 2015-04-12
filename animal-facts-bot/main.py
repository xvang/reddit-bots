import praw
import time
import random
import warnings
import configparser

'''
Requirements:

Python (I used version 3.4.2 to write it. Earlier versions will probably work, but try to get 3.4.2 if you can. It's the latest.)

PRAW
'''

if __name__ =='__main__':
    #We are not using OAuth, so an error will pop up.
    #Soon Reddit will require OAuth to use bots, but for now it's just a warning.
    #To see the warning, just comment out the line below and run the bot.
    #To comment the line out, use the # at the beginning of the line.
    warnings.filterwarnings("ignore")

    config = configparser.ConfigParser()
    config.read('authoriteh.ini')
    name = config.get('reddit_stuff', 'name')
    password = config.get('reddit_stuff', 'password')
    botname = config.get('reddit_stuff', 'botname')
    r = praw.Reddit(user_agent=botname)
    r.login(name, password)


    #This is the keyword you want to search for.
    #For example, the /u/slothsfactbot searches for the keyword "sloth" or "sloths"
    #upper and lower case does not matter. SLOTH is the same as sloth.
    keyword = ""

    message = "fact bot has been summoned!: "
    #For example, /u/slothfactsbot's message is:
    #Did someone mention sloths? Here's a random fact!

    #=============================================#
    #       You don't have to input in anything below this.
    #       But if you know what you're doing, you can always change stuff.
    #=============================================#


    #All the facts go here in 'all_facts'
    #Put in 10 facts, or 10,000 facts. Totally up to you.
    #The important things is to make sure it is formatted properly.
    #single quotations and then a comma and then a new line
    all_facts = ['hello hello hello',
                 'this is the place for facts',
                 'all the facts go here',
                 'in neat sentences',
                 'there are ways to store it outside the code',
                 'but for now this is sufficient for testing',
                 ]

    #'counter' is used to print stuff so we know the bot is working.
    counter  = 0

    #This while-loop is infinite and "runs" the bot.
    while(True):
        
        #The ID of every comment the bot responds to is stored in history.txt
        #The "history = []" reads in all the ID's from history.txt
        #"new_history" contains the new ID's that have been responded to each time the while loop runs.
        #At the end of each "round" of the while loop, the ID's "new_history" is stored into history.txt 
        new_history = []
        history = []
        
        history_file = open("history.txt", "r")

        for h in history_file:
            history.append(h.rstrip('\n'))
        history_file.close()

        #Get the most recent comments. Getting 600 comments every 30 seconds should
        #get most of the new comments made to Reddit.
        #Note: It might take a few seconds.
        all_comments = r.get_comments('all', limit=600)

        #Goes through all the comments and searches for the keyword you want.
        for comment in all_comments:
            
            #'confirmed_new' is a boolean. It will be true if the comment id is not in history
            # and it is not in new_history
            confirmed_new = (comment.id not in history) and (comment.id not in new_history)

            #If the keyword is found in the comment, and it is a totally new comment, we respond!
            if (keyword in comment.body.lower()) and confirmed_new:

                #get a random fact from the list of random facts above.
                random_fact = all_facts[random.randint(0, len(all_facts) - 1)]

                #reply to the comment!
                comment.reply(str(message) + "\n\n---\n\n" + str(random_fact))
                print("Replied to /u/%s" %(comment.author))

                #add it to our history so we don't respond multiple times.
                new_history.append(comment.id)

        #After each while run, we take all the new comment id's that we found,
        #and store it in history.txt
        out = open("history.txt", "a")
        for h in new_history:
            out.write(str(h) + "\n")
        out.close()
        
        counter = counter + 1
        print("finished run #: " + str(counter))

        #Something about reddit caches being 30 seconds, so we pause 30 seconds.
        #It's best to pause for a bit anyways.
        #The more pause we have, the less likely the bot gets caught in some spam filters.
        time.sleep(30)

















        
