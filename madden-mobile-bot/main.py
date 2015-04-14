import praw
import time
import configparser


already_checked = []


def user_reply(info, submission, r):

    message = "#Reputation breakdown for /u/%s \n\n" % (info['username'])

    message = message + "\n\n---\n\n"

    message = message + "Account created: %s \n\n" % (info['created'])

    message = message + "Account age: %s \n\n" % (info['age'])

    if(str(info['link']) == "Rep Profile not found in /r/mcsrep"):
        message = message + str(info['link'])
    else:
        message = message + "[Link to Rep Profile in /r/mcsrep](%s)" % (info['link'])

    message = message + "\n\n---\n\n"

    message = message + "#Info about testimonies made on behalf of /u/%s:\n\n" % (info['username'])
        
    if(len(info['testimonies']) == 0):
        message = message + "No testimonies found.\n\n"
    else:
        message = message + "\n\nName|Account Age(in days)|Karma Count|Link to Their Rep Profile|Comment about /u/%s\n" % (str(info['username']))
        message = message + ":-:|:-:|:-:|:-:|:-:\n"
        for t in info['testimonies']:
            line_in_table = ''
            #info about the testimonies will be shown in a table. so each line is for each testimony.

            if(t['link_to_rep'] == "None"):
                line_in_table = str(t['name']) + "|" + str(t['age']) + "|" + str(t['karma_count']) + "|" + "None" + "|" + str(t['comment'])  + "\n"
            else:
                line_in_table = str(t['name']) + "|" + str(t['age']) + "|" + str(t['karma_count']) + "|" + ("[link](%s) " % (str(t['link_to_rep']))) +  "|" + str(t['comment']) + "\n"
            message = message + line_in_table

        if(info['testimony_amount'] > 10):
            message = message + "\n\n---\n\n"
            message = message + ("/u/%s's Rep Profile has **%s** top-level comments, only **10** is shown above." % (str(info['username']), str(info['testimony_amount'])))
        

        
    try:
        #TODO: add the id of the submission where you want the bot to post to.
        sss = r.get_submission(submission_id='')
        sss.add_comment(message)
        #submission.add_comment(message)
        print("posted review of: /u/%s" %(str(info['username'])))
        
    except:
        print("Could not posted review of: /u/%s" %(str(info['username'])))

    
def fetch_stats(name, r, submission):

    user = r.get_redditor(str(name))
    
    info = {}

    #fetch the time the  account was created.
    created_time = time.strftime("%b-%d-%Y", time.gmtime(user.created_utc))

    #calculate the age of the account.
    age = time.time()  - user.created_utc
    days = 0
    while (age >= 86400):
        age = age - 86400
        days = days + 1
    age_string = str(days) + " days old."


    link_to_reputation = ""
    link_id = ""
    searched = r.search(query=(str('/u/') + str(name)), subreddit="mcsrep",
                        sort="top",period="all", limit=None)

    for s in searched:
        if( str(name).lower() == str(s.author).lower()):
            link_id = s.id
            link_to_reputation = str(s.permalink)

    #if the link was unchanged, that means user's reputation post was not found.
    if link_to_reputation == "":
        link_to_reputation = "Rep Profile not found in /r/mcsrep"
        info['testimonies'] = []

    #else, we fetch info about the testimonials.
    else:
        #'link_id' contains the id of the user's post in /r/mcsrep.
        comments = r.get_submission(submission_id=link_id).comments

        #list of dict's containing info about each user testimony.
        testimonials = []

        #This is to limit the checking the comments.
        #One user had like almost 600 comments in their rep profile,
        #And it took me a stupid amount of time to realize that was
        #why the bot kept crashing.  We're not going to check 600 comments. 
        counter = 0
        good_counter  = 0
        for c in comments:

            counter = counter + 1
            target_comment = c
            #Restrict the number of comments checked to 10.
            if (good_counter <= 10):
                user_testimony = {}

                target_comment = c
                #sometimes the user posts themselves on their rep profile,
                #and the testimonies respond to them.
                #So we need to get comments that are one level down.
                if(str(c.author).lower() == name.lower()):
                    replies = c.replies

                    for reply in replies:
                        if(type(reply) == praw.objects.Comment):
                            if not (str(reply.author).lower() == name.lower()):
                                target_comment = reply


                
                    
                    
                user_testimony['name'] = str(target_comment.author)

                #get the time the commenter created account.
                redditor = r.get_redditor(str(target_comment.author))

                t_age = time.time()  - redditor.created_utc
                t_days = 0
                while (t_age >= 86400):
                    t_age = t_age - 86400
                    t_days = t_days + 1

                user_testimony['age'] = str(t_days)

                #search for the testimony's rep profile in /r/mcsrep.
                searched = r.search(query=(str('/u/') + str(target_comment.author)), subreddit="mcsrep",
                            sort="top",period="all", limit=None)

                llink = "None"
                for s in searched:
                    if( str(target_comment.author).lower() == str(s.author).lower()):
                        llink = s.permalink
                        break

                user_testimony['link_to_rep'] = str(llink)
                

                user_testimony['karma_count'] = str(redditor.link_karma + redditor.comment_karma)

                cc = str(target_comment.body)
                if(len(cc) > 100):
                    cc = str(cc)[:100] + "....."

                user_testimony['comment'] = str(cc).replace("\n", " ")

                if not (user_testimony['name'].lower() == name.lower()):
                    testimonials.append(user_testimony)
                    good_counter = good_counter + 1


        info['testimonies'] = testimonials
        info['testimony_amount'] = counter

    
    info['username'] = str(user)
    info['created'] = str(created_time)
    info['age'] = str(age_string)
    info['link'] = str(link_to_reputation)



    user_reply(info=info, submission=submission, r=r)

    
    

    




def check_subreddit(r, bot_name):

    global already_checked
    
    posted_submissions = r.get_subreddit("maddenmobilebuysell").get_new(limit=6)

    for post in posted_submissions:

        commenters = []
        
        #If we haven't checked the post,
        #If we haven't recorded the username yet.
        #Even if someone comments 5 times on  a submission, we only need to record name once.
        #'commenters' stores the name of everyone who commented.
        buy_sell = ("[buy]" in post.title.lower()) or ("[sell]" in post.title.lower())
        if((str(post.id) not in already_checked) and (buy_sell)):
            if str(post.author) not in commenters:
                commenters.append(str(post.author))

            #if our name was not in list of commenters,
            #that means we haven't posted the stats yet.
            if not (str(bot_name) in commenters):

                #fetch info about the user that made the submission.
                fetch_stats(name=str(post.author), r=r, submission=post)

                already_checked.append(str(post.id))
                time.sleep(20)

        else:
            print("Already checked: ", str(post.author))







if __name__=='__main__':


    #login 
    config = configparser.ConfigParser()
    config.read('auth.ini')
    name = config.get('credentials', 'username')
    password = config.get('credentials', 'password')
    agent = config.get('credentials', 'agent')
    r = praw.Reddit(user_agent=agent)
    r.login(name, password)

    counter = 0
    while(True):

        check_subreddit(r=r, bot_name=name)
        counter = counter + 1

        print("Finished #: " + str(counter))
        time.sleep(120)
