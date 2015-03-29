##Requirements:

praw (Python Reddit API Wrapper)

Python (any version should work, but I used python34)


#What does it do?

It breaks down a specified user's karma by subreddit and returns the results as a message to the user that requested the information.


#How do I ask it to do stuff?

Just send a message with a command in the body of the message.

The options are: 

	"checkme" -- checks the sender's karma
	
	"/u/some_username_" -- checks the username that was sent
	
	
	
#How to run the bot Option #1:

This is for Windows, I'm not sure about any others.

You will need to to have main.py and login.py in the same folder.

You will need to create a file called 'auth.ini' and save it in the same place.

To create an ini file, just create a txt file and rename it 'auth.ini'

Then open up the 'auth.ini' file in any text editor and copy and paste the 4 lines below into it:


[credentials]

username=

password=

botname=




Fill out it out accordingly. Write down an account's username, password, and a name for your bot.
Make your the bot's name is unique and descriptive. Don't name it something like "SOFIOISDJOIJEEE"

Open up IDLE. It should pop up when you search for it. Then open up main.py. Press F5 to run the bot. That's it!



#How to run the bot Option #2:

Comment out line 103. It is "login_info=login.login()" ..... or delete the line. You won't need it.

To comment out a line, put the pound(#) sign in front of it.

Replace line 105 with this: r = praw.Reddit("__name_of_your_bot_goes_here_dont_leave_it_like_this___")

Replace line 106 with this: r.login("username", "password")

This is where you enter in the user name and password for your bot.

Open up IDLE. It should pop up when you search for it. Then open up main.py. Press F5 to run the bot. That's it!

