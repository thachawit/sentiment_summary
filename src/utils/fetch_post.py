import snscrape.modules.twitter as sn_twitter
import pandas as pd

tweet_limit = 50
reply_limit = 100


def query_search(query, limit=True):
    tweets = []
    replies = []

    print("Search query => ", query)

    for tweet in sn_twitter.TwitterSearchScraper(query).get_items():

        if limit and len(tweets) == tweet_limit:
            break
        else:
            print("Fetching tweet posts... ", tweet.id)
            try:
                tweets.append(
                    [tweet.date, tweet.user.username, tweet.renderedContent])
            except AttributeError:
                print("Fetch failed => ", tweet)

            tweet_replies = sn_twitter.TwitterTweetScraper(tweet.id,
                                                           mode=sn_twitter.TwitterTweetScraperMode.SCROLL).get_items()
            count = 0

            print("Fetching replies...")
            for reply in tweet_replies:
                if limit and count == reply_limit:
                    break
                else:
                    if reply.id == tweet.id:
                        replies.append(
                            [reply.date, reply.user.username, reply.renderedContent, ''])
                    else:
                        try:
                            replies.append(
                                [reply.date, reply.user.username, '', reply.renderedContent])
                        except AttributeError:
                            print("Fetch failed => ", reply)
                count += 1

    return replies


def fetch_post_with_reply_by_user(user, start_date, end_date, limit=True):
    query = f"(from:{user}) since:{start_date} until:{end_date} exclude:replies"

    replies_data = query_search(query, limit)

    df = pd.DataFrame(replies_data, columns=['Date', 'User', 'Tweet', 'Reply'])
    print(df)

    return df


def fetch_post_with_reply_by_text(text, start_date, end_date, limit=True):
    query = f"{text} since:{start_date} until:{end_date} exclude:replies"

    replies_data = query_search(query, limit)

    df = pd.DataFrame(replies_data, columns=['Date', 'User', 'Tweet', 'Reply'])
    print(df)

    # Save to csv
    df.to_csv('../data/text_tweets.csv')


# Call function

fetch_post_with_reply_by_user("elonmusk", "2023-03-20", "2023-03-23")
# fetch_post_with_reply_by_text("tesla", "2023-03-22", "2023-03-23")
