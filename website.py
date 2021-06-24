import streamlit as st
import pandas as pd
import dynamo
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import datetime

def find_subreddit(search: str) -> list:
    if not search:
        return []
    exact_match = search
    search = search.lower()
    subreddits = dynamo.subreddits()
    found = []
    for subreddit in subreddits:
        if search in subreddit.lower():
            found += [subreddit]
    for subreddit in found:
        if subreddit == exact_match:
            return [subreddit]
    return found

def convert_timestamp(timestamp: int):
    time = datetime.datetime.fromtimestamp(timestamp)
    return str(time)

def extract_top(sub_counts: list, limit: int) -> (list, list):
    top = []
    tuples = [(row.split()[0], int(row.split()[1])) for row in sub_counts]
    tuples = sorted(tuples, key=lambda x: x[1], reverse=True)[:limit]
    names = []
    counts = []
    for t in tuples:
        names += [t[0]]
        counts += [t[1]]
    return names, counts

def extract_string_from_titles(titles: pd.DataFrame) -> str:
    result = ""
    for title in titles:
        result += f" {str(title)}"
    return result

form = st.form(key='search_form')

form_subreddit = form.text_input(label='Search Subreddit')
form_search = form.text_input(label='Search Title')
submit_button = form.form_submit_button(label='Submit')

# Defaults to prevent crashes
table_contents = [[]]
message = ""
table = None

if submit_button:
    subreddits = find_subreddit(form_subreddit)
    if len(subreddits) == 0:
        message = "No matching subreddit found"
    elif len(subreddits) == 1:
        table_contents = dynamo.query_table_by_title(form_search, subreddits[0])
        if len(table_contents) == 0:
            message = f"No posts with that title found in subreddit {subreddits[0]}"
        else:
            message = f"{len(table_contents)} results found in subreddit {subreddits[0]}"
            # Prepare table
            headings = ['Title', 'Subreddit', 'url', 'timestamp', 'name']
            table = pd.DataFrame(table_contents)
            table.columns = headings
            titles = extract_string_from_titles(table['Title'])
            wordcloud = WordCloud().generate(titles)
            # Apply aesthetic changes to table
            table = table.drop(labels='name', axis=1)
            table['timestamp'] = table['timestamp'].apply(convert_timestamp)
    else:
        message = "Multiple matching subreddits found!\nDid you mean one of these:  \n"
        for s in subreddits:
            message += f"{s}  \n"
        message = message[:-1]

    st.write(message)

    if type(table) is pd.DataFrame:
        st.write(table)
        # Display wordcloud
        st.markdown("<center>Most used words Word Cloud</center>", unsafe_allow_html=True)
        fig, ax = plt.subplots(1, 1)
        plt.imshow(wordcloud)
        plt.axis("off")
        st.pyplot(fig)

else:
    # Main page before search
    sub_counts = dynamo.get_subreddit_counts()
    names, counts = extract_top(sub_counts, limit=30)
    
    # Display popular subreddits chart
    fig, ax = plt.subplots(1, 1)
    ax.bar(names, counts)
    ax.set_title("Top Subreddits")
    ax.set_xlabel('Subreddit')
    ax.set_ylabel('Number of Posts')
    ax.set_xticklabels(names, rotation=90)
    st.pyplot(fig)