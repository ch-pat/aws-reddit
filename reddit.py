import praw
import time
import os
import dynamo


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

    items = []
    for s in lista:
        items += [(s.name, s.title, s.url, s.num_comments, s.created_utc, s.subreddit)]
    return items

if __name__ == "__main__":


    table = dynamo.get_posts_table()
    start_time = time.time()

    for i in range(TOTAL_POSTS // LIMIT):
        posts = get_posts()
        count = 0
        with table.batch_writer(overwrite_by_pkeys=['name', 'timestamp']) as batch:
            for post in posts:
                time.sleep(0.2)
                count += 1
                batch.put_item(
                    Item={
                        'name': str(post[0]),
                        'title': str(post[1]),
                        'url': str(post[2]),
                        'num_comments': int(post[3]),
                        'timestamp': int(post[4]),
                        'subreddit': str(post[5])
                    }
                )
        time.sleep(5)
        print(f"Currently at iteration {i} of {TOTAL_POSTS // LIMIT}")
        print(f"Elapsed time: {time.time() - start_time}")
        print(f"Added {count} posts")


