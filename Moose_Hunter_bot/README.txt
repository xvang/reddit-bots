bot requested by /u/queequeger

This README only a few paragraphs. Please read the whole thing! 


This is a Reddit Bot made to respond to a specific user.

To run the program, just double click the "reddit_bot_2.py".
To edit stuff in the program, you have to open the file "reddit_bot_2.py" in a text editor.
If you're on Windows you can use NotePad, or NotePad++
I am not familiar with Mac or Linux or anything other than Windows, 
but any text editor should work.

And if it just totally breaks down and doesn't work, feel free to send me a message.
And it's running from your computer and not a dedicated server, so once the computer 
shuts down the program stops. You will need to manually start the program every time.


HOW TO RUN THE BOT:
You need python 3.3.2 and praw installed. 
Open the .bat file in a text editor. Edit in the path to the reddit_bot_2.py file. Save it. 
Then just double click the bat file!

HOW IT WORKS:

It retrieves the most recent 10 comments made by the user you are targetting.
Then it checks that against a list of comments that it has already responded to (saved in history.txt). 
If any of the 10 recent comments have not been responded to, then the bot will respond to it.
After responding, the bot will save the comment into the file (history.txt) so it won't respond multiple times.
That's it!

The bot(/u/Moose_Hunter_Bot) is a new user, so it can only post once every 10 minutes. 
So currently, if there are 10 new comments, then it can take the bot 
up to 100 minutes to respond to all the comments.
The good new is that after a while, you can change it so that the bot posts instantly.
Don't worry, I explain how to change it below.


HOW TO MAKE CHANGES TO THE BOT:

There is a section in the source code file that I labelled "Change Stuff Here".
You can change stuff like the message and how active the bot will be.
There are variables that you can change the value of.


"self.message": 
	This is the message that the bot will respond with. I don't know if it can work with fancy ascii or 
	comments with signatures. But it should work fine if you want the bot to respond with a sentence or two. 
	In the program you will see something like this: self.message = ""
	Put your message between the quotations.
	
	
"self.RUN_FOREVER":
	When you set this to True(capital T, it's important!), that means the bot will run forever, or 
	until you turn off your computer. Every so often it will run and check for new comments made
	by the user.
	If this is set to False(capital F), then it will only run once and then it will end. 
	
	
"self.period":
	If "self.RUN_FOREVER" is set to True, then this variable comes into play. 
	This controls how often the program runs. So for example, if self.period = 600,
	then every 600 seconds, the program will run. It's good to have the program 
	wait a few minutes between each run.  Bots that send infinite requests to Reddit servers
	are part of the reason why Reddit crashes so often.
	
"self.target_User":
	This is the user you want to target. I set it to /u/-moose- but you can target whoever you want.
	You don't need to include the "/u/" part. 
	
"self.pause":
	This is how long the bot waits before posting. Currently it is a new user so it can
	only post once every 10 minutes. But once it loses it's "noob" status and is able to 
	post without the 10 minute penalty, you should change it so it doesn't wait 10 minutes.
	
	Right now it's like this: self.pause = 630 , it pauses for 10 and a half minutes.
	You should change it to a smaller number or even zero: self.pause = 0
	

"self.login_name":
	The login name of the bot. If you don't want to use the user "Moose_Bot_Hunter"
	then create a new user and put its name in this variable
	self.login_name = 'new_user_name'
	self.login_password = 'new_password'
	
"self.bot_name":
	This is the name Reddit will identify the bot by when it communicates with the Reddit servers.
	It can be a name or a code, but it should be unique to this bot. 
	To change the name, put whatever name you want in between the parenthesis.
