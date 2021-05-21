import praw
import time
import os

FOLDER = 'posts'
LIMIT = 500                 # How many posts to download at each iteration
POSTS_PER_FILE = 200000     # Number of posts saved in each file
TOTAL_POSTS = 1000000       # Total posts to download
TOTAL_FILES = TOTAL_POSTS // POSTS_PER_FILE

def save_to_disk(filename: str, rows_to_add: str):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(rows_to_add)

def get_posts() -> str:
    reddit = praw.Reddit(
    client_id="YPyVQ6b1OdrwgQ",
    client_secret="KceGXwiCg6qnvNCgvTTHUMiBW5PJ8g",
    password="MegaSukamon",
    user_agent="cammellogigante",
    username="MegaSukamon",
    )
    lista = reddit.subreddit('all').new(limit=LIMIT)

    rows = ""
    for s in lista:
        rows += f"{s.name}|||{s.title}|||{s.url}|||{s.num_comments}|||{s.created_utc}\n"
    return rows

if __name__ == "__main__":
    if not os.path.isdir(FOLDER):
        os.mkdir(FOLDER)

    for n in range(TOTAL_FILES):
        filename = str(n)
        filepath = os.path.join(FOLDER, filename)
        iterations = POSTS_PER_FILE // LIMIT
        for _ in range(iterations):
            rows = get_posts()
            save_to_disk(filepath, rows)
            time.sleep(5)
