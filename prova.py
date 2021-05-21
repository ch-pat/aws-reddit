import praw
reddit = praw.Reddit(
    client_id="YPyVQ6b1OdrwgQ",
    client_secret="KceGXwiCg6qnvNCgvTTHUMiBW5PJ8g",
    password="MegaSukamon",
    user_agent="cammellogigante",
    username="MegaSukamon",
    )
lista = reddit.subreddit('all').new(limit=10)
for l in lista:
    print(str(l.subreddit))