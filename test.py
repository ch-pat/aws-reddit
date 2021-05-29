import streamlit as st
import pandas as pd
import dynamo

def find_subreddit(search: str) -> str:
    search = search.lower()
    subreddits = dynamo.subreddits()
    for subreddit in subreddits:
        if search in subreddit.lower():
            return subreddit

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
    st.write(table)
else:
    # Pagina principale prima della ricerca
    dynamo.get_subreddit_counts()
    st.write('siamo nell else')