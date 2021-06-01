import streamlit as st
import pandas as pd
import dynamo
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def find_subreddit(search: str) -> str:
    search = search.lower()
    subreddits = dynamo.subreddits()
    for subreddit in subreddits:
        if search in subreddit.lower():
            return subreddit

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


with st.form(key='search_form'):
    form_subreddit = st.text_input(label='Search Subreddit')
    form_search = st.text_input(label='Search Title')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    subreddit = find_subreddit(form_subreddit)
    if subreddit:
        table_contents = dynamo.query_table_by_title(form_search, subreddit)
        message = f"{len(table_contents)} results found in subreddit {subreddit}"
    else:
        message = "No matching subreddit found"
    
    st.write(message)
    # Prepara tabella
    headings = ['Title', 'Subreddit', 'url', 'timestamp', 'name']
    table = pd.DataFrame(table_contents)
    table.columns = headings

    titles = extract_string_from_titles(table['Title'])
    wordcloud = WordCloud().generate(titles)

    st.write(table)

    # Display wordcloud
    st.markdown("<center>Most used words Word Cloud</center>", unsafe_allow_html=True)
    fig, ax = plt.subplots(1, 1)
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)
else:
    # Pagina principale prima della ricerca
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