import GetOldTweets3 as got
import pandas as pd
import os
import glob
from tqdm import tqdm
from utilities.path_dataset import get_folder_path


def mergeFiles(extension="csv", path=None,output_file='combined_file'):
    """
    Merge files from a specific folder in a specific format
    :param extension: format of the file (for example: csv)
    :param path: custom path where you want to save the csv
    :return:
    """
    

    if path is None:
        base_path = get_folder_path('./')
    else:
        base_path = path
    try:
        print(f'Basepath: {base_path}')
        
        file_list_path = os.path.join(base_path,'tweets_downloaded')
        print(f'Reading and parsing all csv downloaded from: {file_list_path}')
        os.chdir(file_list_path)
    
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

        # combine all files in the list
        combined_csv = pd.concat([pd.read_csv(f, sep=";") for f in all_filenames])

        # Parse the file and remove special chars (avoid errors into lucene indexes)
        colnames = combined_csv.columns
        combined_csv[colnames] = combined_csv[colnames].replace({';': ''}, regex=True)

        # export to csv
        file_name = os.path.join(base_path,"results",output_file + '.' + extension)
        combined_csv.to_csv(file_name, index=False, sep=";", encoding='utf-8-sig')

        print(f"Files combined into: {file_name}")
        return True

    except Exception as message:
        print(f"Impossible to concat the file into: {base_path} because: {message}")
        return False


def writeTweetDisk(tweet_collection, collection_name, folder=None, path=None):
    """
    Write a tweet to disk
    :param tweet_collection: object containing tweets
    :param collection_name: name of the collection
    :param folder: folder you want to save the tweets
    :param path: optional pat if you want to export tweets outside the main folder
    :return: boolean (True, False)
    """
    # Create the tweets collection
    tweets = pd.DataFrame()
    permalink_list = []
    username_list = []
    text_list = []
    date_list = []
    retweets_list = []
    favorite_list = []
    mentions_list = []
    hashtag_list = []
    geo_list = []

    # Obtain data from the tweet_collection object
    tweet_len = tweet_collection.__len__()
    for t in tqdm(range(tweet_len)):
        permalink_list.append(tweet_collection[t].permalink)
        username_list.append(tweet_collection[t].username)
        text_list.append(tweet_collection[t].text)
        date_list.append(tweet_collection[t].date)
        retweets_list.append(tweet_collection[t].retweets)
        favorite_list.append(tweet_collection[t].favorites)
        mentions_list.append(tweet_collection[t].mentions)
        hashtag_list.append(tweet_collection[t].hashtags)
        geo_list.append(tweet_collection[t].geo)

    # Populate the dictionary for the export
    tweets["permalink"] = permalink_list
    tweets["username"] = username_list
    tweets["text"] = text_list
    tweets["date"] = date_list
    tweets["retweet"] = retweets_list
    tweets["favorite"] = favorite_list
    tweets["mentions"] = mentions_list
    tweets["hashtag"] = hashtag_list
    tweets["geo"] = geo_list

    tweets.index.name = "id"

    # Parse the file and remove special chars
    colnames = tweets.columns
    tweets[colnames] = tweets[colnames].replace({';': ''}, regex=True)

    # Write to disk
    # Set the path for the file
    base_path = os.path.abspath('')

    if path is not None:
        file_path = path
    else:
        file_path = base_path

    file_name = collection_name + '.csv'

    if folder is not None:
        export_path = os.path.join(file_path, folder, file_name)
    else:
        export_path = os.path.join(file_path, file_name)

    try:
        tweets.to_csv(export_path, sep=";")
        print(f"Collection of tweet: {collection_name} exported successfully to: {export_path}")
        return True
    except Exception as message:
        print(f"Impossible to generate the csv to {export_path} because: {message}")
        return False


def printTweet(description, tweets):
    """
    Print the tweet you have downloaded
    :param description: custom user description of the tweet
    :param tweets: collection of tweets you want to view
    :return: nothing
    """
    print(description)
    tweet_len = tweets.__len__()
    for t in range(tweet_len):
        print("Username: %s" % tweets[t].username)
        print("Retweets: %d" % tweets[t].retweets)
        print("Text: %s" % tweets[t].text)
        print("Mentions: %s" % tweets[t].mentions)
        print("Hashtags: %s\n" % tweets[t].hashtags)


def downloadWithUsername(username, since=None, until=None, collection_name=None, max_tweets=1000, print=False):
    """
    # Mode 1 - Get tweets by username
    :param collection_name: name of the tweet collection
    :param until: initial date for the research
    :param since: final date for the research
    :param username: username for the research
    :param max_tweets: maximal number of tweets
    :return:
    """

    if since is None or until is None:
        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setMaxTweets(max_tweets)
        tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    # Research since and until a date
    else:
        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(since).setUntil(
            until).setMaxTweets(max_tweets)
        tweet = got.manager.TweetManager.getTweets(tweetCriteria)

    if print:
        # Print results
        printTweet(f"Tweet from {username}", tweet)

    # Write the tweet to disk
    if collection_name is None:
        writeTweetDisk(tweet, username, "./tweets_downloaded")
    else:
        writeTweetDisk(tweet, collection_name, "./tweets_downloaded")

    return True


def downloadWithQuerySearch(query, username=None, since='2015-01-01', until='2020-02-02', collection_name=None,
                            max_tweets=1000, print=False):
    """
    Download tweets based on a specific query and optionally a date
    :param query: the query you want to use for the research
    :param since: start date for the research
    :param until: end date for the research
    :param collection_name: name of the collection you want to export
    :param max_tweets: max number of tweets you want to download
    :return:
    """

    # Example 2 - Get tweets by query search
    if username is None:
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(since).setUntil(
            until).setMaxTweets(max_tweets)

    else:
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setUsername(username).setSince(
            since).setUntil(
            until).setMaxTweets(max_tweets)

    tweet = got.manager.TweetManager.getTweets(tweetCriteria)

    if print:
        # Print results
        printTweet(f"Tweet with query: {query} since: {since}, until: {until}", tweet)

    # Write the tweet to disk
    if collection_name is None:
        writeTweetDisk(tweet, query, "./tweets_downloaded")
    else:
        writeTweetDisk(tweet, collection_name, "./tweets_downloaded")

    return True
