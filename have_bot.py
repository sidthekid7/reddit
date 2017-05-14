import praw
import prawcore
import re
import time
import os

# JSON structure
# https://github.com/reddit/reddit/wiki/JSON
# reading / writing files: https://docs.python.org/3/tutorial/inputoutput.html

def sleeper():
    time.sleep(2)

def have_fixer():
    reddit = praw.Reddit('bot1')

    # create text file with all banned subreddits
    if not os.path.isfile("banned_subreddits.txt"):
        banned_subreddits = ""
    else:
        with open("banned_subreddits.txt", 'r') as f:
            banned_subreddits = f.read()
            print("List of all banned subreddits: " + banned_subreddits)

    subreddit = reddit.subreddit("all" + banned_subreddits)
    print("all" + banned_subreddits)
    print("Logged in and beginning search")

    # constants
    fixes = 0
    sleep_text = ", Sleeping for 2 seconds"

    # list of fixes
    must_have = "Must have"
    would_have = "Would have"
    could_have = "Could have"
    should_have = "Should have"
    # fixer
    for comment in subreddit.stream.comments():
        try:
            if re.search("must of ", comment.body, re.IGNORECASE):
                if not re.search("must of course", comment.body, re.IGNORECASE):
                    comment.reply(must_have)
                    print(must_have)
                    fixes+=1
                    print("Total fixes: ", fixes, sleep_text)
                    sleeper()

            if re.search("would of ", comment.body, re.IGNORECASE):
                if not re.search("would of course", comment.body, re.IGNORECASE):
                    comment.reply(would_have)
                    print(would_have)
                    fixes+=1
                    print("Total fixes: ", fixes, sleep_text)
                    sleeper()

            if re.search("could of ", comment.body, re.IGNORECASE):
                if not re.search("could of course", comment.body, re.IGNORECASE):
                    comment.reply(could_have)
                    print(could_have)
                    fixes+=1
                    print("Total fixes: ", fixes, sleep_text)
                    sleeper()

            if re.search("should of ", comment.body, re.IGNORECASE):
                if not re.search("could of course", comment.body, re.IGNORECASE):
                    comment.reply(should_have)
                    print(should_have)
                    fixes+=1
                    print("Total fixes: ", fixes, sleep_text)
                    sleeper()
        # catch rate limit error
        except praw.exceptions.APIException as e:
            print("Rate Limit error: ", e.message)
            print("Sleeping for 2 mins and trying again")
            time.sleep(120)

        # write banned subreddits to file
        except prawcore.exceptions.Forbidden:
            current_sub = str(comment.subreddit)
            print("Banned from current subreddit: " + current_sub)
            with open("banned_subreddits.txt", 'a') as f:
                f.write("-" + current_sub)
        except:
            print("Something went wrong, sleeping for 30 seconds")
            time.sleep(30)

if __name__ == "__main__":
    have_fixer()