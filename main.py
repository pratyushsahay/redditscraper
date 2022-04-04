import praw
import pandas as pd
from praw.models import MoreComments
import re

reddit = praw.Reddit(client_id='53i-DXPPcW-utg', client_secret='3cwgb2fJE9zCmn0uPX3M7gpaFk8niA', user_agent='wsb-scraper')

# Pull hot 1000 posts from WSB and write it to csv
# posts = []
# wsb = reddit.subreddit('wallstreetbets').hot(limit=1000)

# for post in wsb:
#     posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])

# posts = pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
# posts.to_csv('wsb_data.csv')

# Get all tickers from nasdaq and nyse dataset
nasdaq = pd.read_csv("nasdaq.csv")
nyse = pd.read_csv("nyse.csv")

nq_tickers = nasdaq['Symbol']
nyse_tickers  = nyse['Symbol']

# Combine nq_tickers and nyse_tickers into one df and remove duplicates
frames = [nq_tickers, nyse_tickers]
result = pd.concat(frames)

remove_dups = result.to_frame().drop_duplicates()

# Count number of mentions of all tickers in WSB post titles
wsb_data = pd.read_csv("wsb_data.csv")
wsb_titles = wsb_data['title']

ticker_counter = {}
remove_ticker = ['OC', 'DD', 'A', 'GOOD', 'ON', 'REAL', 'RUN']

for index, row in remove_dups.iterrows():
    ticker = row['Symbol']
    if ticker not in remove_ticker:
        for index, title in wsb_titles.items():
            if re.search(r'\b' + ticker + r'\b', title):
                if (ticker in ticker_counter):
                    ticker_counter[ticker] = ticker_counter[ticker] + 1
                else:
                    ticker_counter[ticker] = 1

ticker_counter_df = pd.DataFrame.from_dict(ticker_counter, orient='index')
ticker_counter_df.columns = ['Count']

ticker_count_sorted = ticker_counter_df.sort_values(by=['Count'], ascending=False)
ticker_count_sorted.to_csv('ticker_counts.csv')

# Count number of mentions of all tickers in WSB post comments

# Scrape comment test
# url = 'https://www.reddit.com/r/wallstreetbets/comments/mnpcv0/weekend_discussion_thread_for_the_weekend_of/'
# submission = reddit.submission(url=url)
# f = open("test.txt", "a")

# for top_level_comment in submission.comments:
#     if isinstance(top_level_comment, MoreComments):
#         continue
#     # print(top_level_comment.body)
#     f.write("" + top_level_comment.body)

# f.close()