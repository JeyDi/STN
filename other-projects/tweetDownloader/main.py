from utilities.settings import downloadWithUsername, downloadWithQuerySearch, mergeFiles
from parsing.clean import read_tweets_dictionary, keep_columns, simple_parse, tokenization, lemmatize
from datetime import date


def clean_tweets(df=None):
    # Read tweet file if not passed as argument
    if df is None:
        df = read_tweets_dictionary()

    # Keep usefull columns
    df = keep_columns(df)

    # Parse simple special characters from text
    df = simple_parse(df, 'text')

    print("Tokenizing and Stemming text")
    df['text_clean'] = df['text'].apply(tokenization)

    print("Lemmatize (short, long) text")
    df['text_lemma_short'] = df['text_clean'].apply(lemmatize)
    df['text_lemma_long'] = df['text'].apply(lemmatize)

    print(df.columns)

    print("Tweets cleaned succesfully")
    return True


# Documentation
# https://github.com/Jefferson-Henrique/GetOldTweets-python
def main():
    """
    Main common function, the functionalities are:
    - Download tweets
    - Arrange tweets in a single final file (merging)
    """

    print("-- Custom Tweet Downloader --")

    # Keywords are: Politics, Science, Sport, Lifestyle, Tech
    # keywords = ["politics","science","sport","lifesyle","tech"]
    #
    # for k in keywords:
    #     print(f"Downloading tweets for keyword: {k}")

    today = date.today()
    today = today.strftime("%Y-%m-%d")
    print("Today's date:", today)

    # Conte Tweets
    # downloadWithQuerySearch("politics", username="BBCPolitics", collection_name="politics_1", max_tweets=3000)
    downloadWithUsername('@GiuseppeConteIT', since='2020-02-01', until=today, collection_name='conte', max_tweets=10000)
    downloadWithUsername('@matteosalvinimi', since='2020-02-01', until=today, collection_name='salvini',
                         max_tweets=10000)
    downloadWithUsername('@MinisteroSalute', since='2020-02-01', until=today, collection_name='ministero-salute',
                         max_tweets=10000)
    downloadWithUsername('@Palazzo_Chigi', since='2020-02-01', until=today, collection_name='palazzo-chigi',
                         max_tweets=10000)
    downloadWithUsername('@luigidimaio', since='2020-02-01', until=today, collection_name='dimaio', max_tweets=10000)
    downloadWithUsername('@matteorenzi', since='2020-02-01', until=today, collection_name='renzi', max_tweets=10000)
    downloadWithUsername('@zingaretti', since='2020-02-01', until=today, collection_name='zingaretti', max_tweets=10000)
    downloadWithUsername('@DPCgov', since='2020-02-01', until=today, collection_name='protezione-civile',
                         max_tweets=10000)

    downloadWithQuerySearch("coronavirus", username="@LaStampa", collection_name="la-stampa", max_tweets=10000)
    downloadWithQuerySearch("coronavirus", username="@Corriere", collection_name="corriere", max_tweets=10000)
    downloadWithQuerySearch("coronavirus", username="@sole24ore", collection_name="sole24ore", max_tweets=10000)
    downloadWithQuerySearch("coronavirus", username="@fattoquotidiano", collection_name="fattoquotidiano",
                            max_tweets=10000)
    downloadWithQuerySearch("coronavirus", username="@LA7tv", collection_name="fattoquotidiano", max_tweets=10000)

    # Merge the result into a single file
    result = mergeFiles()

    return True


if __name__ == '__main__':
    # Launch the download and the merging
    # result = main()

    # Merge the result into a single file
    # result = mergeFiles()

    # Clean tweets
    result = clean_tweets()

    print(result)
