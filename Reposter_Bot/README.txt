


This goes through a subreddit's archived post and reposts them.


Requirements:
Python (I made it using 3.3.2, but a different version should work. Probably. Hopefully.)

PRAW (reddit wrapper in python)
	



CONTROL:

In repost_bot.py, there is a section labeled: "Change The Stuff Below"
That's where you can change stuff about the bot.

You can check more than one sub for archived stuff.

To do so, you edit the "self.check_these_sub" in repost_bot.py like this:

self.check_these_sub = ["sub_name_1",
						"sub_name_2",
						"sub_name_3",
						"sub_name_etc",
						]

There are more explanations in the code.



HOW IT WORKS:
The bot gets a certain amount of posts from the top all time posts. 
Those are the mosty likely to be archived.

It then checks the id of the posts against the list of id in history.txt
If the post id is not in history.txt, then it hasn't been reposted yet.
Then it will be reposted.

Only the top level comments with a url somewhere in it are reposted. 


						
						

NOTE:
None of the url are not checked. 
The url may lead to an unsafe site or it may not exist any more.

New users can only post once every 10 minutes, and sometimes
they have to do the captcha verification thing.










