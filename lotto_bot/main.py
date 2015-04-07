import praw
import time
from bs4 import BeautifulSoup
import urllib
import warnings
import configparser
import time
import random

from player import Player


def init(player, r):

    #get the user's id, and their id converted to a list
    target_user = r.get_redditor(player.username)
    player.user_id=target_user.id
    id_list = list(target_user.id)


    alphabet  = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7,
                 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14,
                 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21,
                 'v':22, 'w':23, 'x':24, 'y':25, 'z':26
                 }

    for i in range(0, len(id_list)):

        #elements in id_list are char, even if they represent numbers.
        #If they represent numbers, we should be able to just convert them to int.
        #else, we convert them with the alphabet dict.
        try:
            id_list[i] = int(id_list[i])
        except:
            id_list[i] = alphabet[str(id_list[i]).lower()]


    
    for x in id_list:

        id_list.remove(x)
        current_number = x
        
        #if we removed it, and it is still in the list when we check, then there must be at least two of them.
        #we must generate a new unique number within 1-39
        #else, it was not in the list, and we add it back into the list.

        #3 cases:
        #1st case: we change the number to the length of the username
        #2nd case: we change the number to twice the length of the username modulus 39 and then add 1
        #If that still leads to a duplicate number, then the user doesn't get 5 numbers.
        get_five = True
        if(current_number in id_list):
            current_number = len(str(player.username))

        if(current_number in id_list):
            current_number = ((len(str(player.username))*2 ) % 39)+ 1

        if(current_number in id_list):
            get_five = False
            player.lost_number_message = "(Your id kept getting duplicate numbers, so you don't get 5 numbers.)"
        


        if(get_five):
            id_list.append(current_number)
            

        




    #If the user's list had more than 5 digits, we chop off the extra digits.
    if(len(id_list) > 5):
        id_list = id_list[:5]

    #if the user's list had less than 5 digits, we add a message.
    if(len(id_list) < 5):
        player.lost_number_message = "(Your id is funky, so you don't get 5 numbers.)"
    player.numbers = id_list



def check_the_numbers(player):
    history = open("DownloadAllNumbers.txt", "r")

    #this keeps track of the number of days.
    #we need the number of days because the cost to play is $1 a day.
    history_counter = 0
    
    for h in history:
        history_counter = history_counter + 1
        #'day' holds the winning numbers for each day.
        day = h.split()[5:]

        #the numbers are still in 'char' format.
        for d in range(0, len(day)):
            day[d] = int(day[d])

        #get the date
        date = h.split()[2:5]

        #counts the amount of numbers that matched.
        match_counter = 0

        #iterate through the user's numbers,
        #for each one that is in the winning numbers, 'match_counter' goes up by 1
        for u in player.numbers:
            if(u in day):
                match_counter = match_counter + 1


        if(match_counter == 3):
            player.three_correct = player.three_correct + 1
        elif(match_counter == 4):
            player.four_correct = player.four_correct + 1
            player.match_four_dates.append("%s-%s-%s .......... %s,%s,%s,%s,%s" %(date[0], date[1], date[2], day[0], day[1], day[2], day[3], day[4]))
            
        elif(match_counter == 5):
            player.five_correct = player.five_correct + 1
            m = "On this day, " + ("%s %s %s, /u/%s's converted Reddit ID# matched the California Fantasy Five lottery numbers. " % (date[0], date[1], date[2], player.username))

            #add message to player object.
            player.messages.append(m)

    player.history_size = history_counter


def print_results(player):

    print("Assuming a match-3 is worth $15, a match-4 is worth $450, and a match-5 is worth $50,000, and we ignore inflation")
    print("User: %s " % (player.username))
    print("User ID: %s " % (player.user_id))
    print("User's Numbers: %s, %s, %s, %s, %s " %(str(player.numbers).replace("[","").replace("]","")))

    
    print("3-match: %s" % (player.three_correct))
    print("4-match: %s" % (player.four_correct))
    print("5-match: %s" % (player.five_correct))

    #player.message contains sentences: "On this day,....."
    for m in player.messages:
        print(m)

    print("Cost of tickets: $", player.history_size)

    money_won = player.three_correct*15 + player.four_correct*450 + player.five_correct*50000
    print("Total money won: $", money_won)



def reply_message(player, r):

    title = "lotto-bot response"

    message = ""

    message = message + "Name: %s \n\n" % (player.username)
    message = message + "ID: %s  \n\n" % (player.user_id)
    message = message + "User's Numbers: %s %s \n\n" %(str(player.numbers).replace("[","").replace("]",""), player.lost_number_message)

    message = message + "3-match: %s \n\n" % (player.three_correct)
    message = message + "4-match: %s \n\n" % (player.four_correct)
    message = message + "Match-4 dates: \n\n"

    for m in player.match_four_dates:
        message = message + m + "\n\n"
        
    message = message + "5-match: %s \n\n" % (player.five_correct)

    for m in player.messages:
        message = message + m + "\n\n"

    message = message + "\n\n---\n\n"
    message = message + "Numbers are from [California Lottery Fantasy Five](http://www.calottery.com/play/draw-games/fantasy-5).\n\n"
    message = message + "Assuming a match-3 is worth $15, a match-4 is worth $450, and a match-5 is worth $50,000, and we ignore inflation:\n\n"
    
    message = message + "Cost to play every day: $%s  \n\n" % player.history_size

    money_won = player.three_correct*15 + player.four_correct*450 + player.five_correct*50000

    message = message + "Total money won: $%s  \n\n" % money_won


    try:
        r.send_message(player.username, title, message)
        print("Sent message to /u/%s" %(str(player.username)))
    except:
        print("Could not send message")
    
    

def reply_comment(player):

    message = ""
    message = message + "Name: %s \n\n" % (player.username)
    message = message + "ID: %s  \n\n" % (player.user_id)
    message = message + "User's Numbers: %s %s \n\n" %(str(player.numbers).replace("[","").replace("]",""), player.lost_number_message)
    message = message + "3-match: %s \n\n" % (player.three_correct)
    message = message + "4-match: %s \n\n" % (player.four_correct)
    message = message + "5-match: %s \n\n" % (player.five_correct)

    for m in player.match_four_dates:
        message = message + m + "\n\n"
        
    for m in player.messages:
        message = message + m + "\n\n"

    message = message + "\n\n---\n\n"
    message = message + "Numbers are from [California Lottery Fantasy Five](http://www.calottery.com/play/draw-games/fantasy-5).\n\n"
    message = message + "Assuming a match-3 is worth $15, a match-4 is worth $450, and a match-5 is worth $50,000, and we ignore inflation:\n\n"

    money_won = player.three_correct*15 + player.four_correct*450 + player.five_correct*50000

    message = message + "Cost to play every day: $%s  \n\n" % player.history_size
    
    message = message + "Total money won: $%s  \n\n" % money_won

    return message

def test_run(r):
    player = Player()

    player.username="sarah"

    init(player=player, r=r)

    check_the_numbers(player=player)

    reply_message(player=player, r=r)
    
def run(name, r):
    #player object.
    player = Player()

    #store the username into the player object.
    player.username=name

    #calculates the user's 5 numbers.
    init(player=player, r=r)

    #checks the user's numbers against the past lottery numbers.
    check_the_numbers(player=player)

    
    #print_results(player=player)

    reply_message(player=player, r=r)


def comment_run(name,r, comment):

    player = Player()
    player.username=name
    init(player=player, r=r)
    check_the_numbers(player=player)

    message = reply_comment(player=player)
    
    #Reply to comment is done here.
    try:
        comment.reply(message)
        print("Responded to /u/%s" % (name))
    except:
        print("Could not respond")
        
def check_mail(r):

    #retrieve unread mail.
    unread = r.get_unread(limit=None)

    for u in unread:
        if (u.body.lower() == "checkme"):
            run(name=u.author, r=r)
        else:
            r.send_message(u.author, "Nope", "please message \"checkme\" .... without the quotations.")
        u.mark_as_read()

def check_thread(r):

    #history.txt contains all previously responded-to comments.
    history_file = open("history.txt")
    history = []
    new_comments = []
    for h in history_file:
       history.append(h.rstrip('\n'))

    history_file.close()
    submission = r.get_submission(submission_id='')

    #Get only the top level comments.
    comments = submission.comments


    for c in comments:
        if (str(c.body).lower() == "checkme") and (c.id not in history):
            comment_run(name=c.author, r=r, comment=c)
            new_comments.append(c.id)


    #add the new_comments back into history.txt
    o = open("history.txt", "a")
    for n in new_comments:
        o.write(str(n) + "\n")
    o.close()

if __name__ == '__main__':

    #some deprecation warning kept popping up, so this is here now.
    warnings.filterwarnings("ignore")


    #login 
    config = configparser.ConfigParser()
    config.read('auth.ini')
    name = config.get('credentials', 'username')
    password = config.get('credentials', 'password')
    botname = config.get('credentials', 'botname')
    r = praw.Reddit(user_agent=botname)
    r.login(name, password)


    counter = 0
    while(True):
        
        #check mail
        check_mail(r=r)
    
        #Check specific thread.
        check_thread(r=r)

        #for testing purposes. 
        #test_run(r=r)
        counter = counter + 1
        print("finished: #", counter)
        
        #sleep for 10 seconds.
        time.sleep(20)





    
