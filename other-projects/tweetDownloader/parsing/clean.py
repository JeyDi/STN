import os
import nltk
import re
import spacy
from tqdm import tqdm
import pandas as pd
from utilities.path_dataset import get_folder_path, read_dataset, save_dataset
from utilities.yaml import read_yaml, write_yaml

nlp = spacy.load('it_core_news_sm', parse=True, tag=True, entity=True)


# 1. Import the full csv with tweets
def read_tweets_dictionary(filename=None, path=None):
    """
    Read the complete tweets dictionary after the merge
    Please consider to sep the merge file with ; char

    """
    if path is None:
        path = './results'

    base_path = get_folder_path(path)

    if filename is None:
        filename = 'combined_file.csv'

    file_path = os.path.join(base_path, filename)

    try:
        dataset = read_dataset(file_path, csv_sep=';')
        print(f'Dataset readed: {file_path}')
        return dataset

    except Exception as message:
        print(f'Impossibile to read the dataset: {message}')
        return None


# 2. Delete unusefull columns (keep only usefull)
def keep_columns(dataset, keep_columns=None, path=None, filename=None):
    """
    Keep only usefull columns into tweets dataset for analysis
    """
    if filename is None:
        filename = 'columns.yml'

    # Import columns from file yml
    if keep_columns is None:
        keep_columns = read_yaml('./resources', filename)

    dataset = dataset[keep_columns]

    print(f'Columns selected: ', keep_columns)

    return dataset


# 3. Parse punctuaction
def simple_parse(dataset, column, list_tokens=None):
    """
    Remove set of tokens (punctuaction and other)
    You can also set a handly list of tokens you want to parse (from outside)
    Dataset have to be a pandas dataframe
    """
    if not isinstance(dataset, pd.DataFrame):
        print("Please use a pandas dataframe as input")
        pass

    print("Start cleaning the dataset")

    # Clean nan or empty text
    dataset = dataset.dropna(subset=['username', 'text', 'date'])

    # Replace unwantend symbols into tweet text
    try:
        # dataset['text'].replace(to_replace="\w+.*", value='',regex=True)
        df_column = dataset[column]
        replaced = []
        for i, t in tqdm(enumerate(df_column)):
            t = re.sub('[^A-Za-z ]+', '', t)
            t = t.lower().strip()
            replaced.append(t)

        dataset = dataset.drop(column, axis=1)
        dataset[column] = replaced

        print("Dataset parsed: deleted nulls, got only chars plus lower and strip editing")
        return dataset
    except Exception as message:
        print(f"Error: {message}")
        # print(f"Impossible to parse the string: {i} in the dataframe for text: {t}")
        return None


def count_words(df, column):
    """
    Count the number fo words in a dataframe
    :param df: input dataframe with words
    :param column: column you want to count words
    :return: number of words
    """
    n_words = df[column].apply(lambda x: len(x.split(' '))).sum()

    print('Number of words', n_words)

    return n_words


def lemmatize(text):
    """
    Lemmatize words using NLP Spacy package
    :param nlp: Spacy NLP function
    :param text: Text to lemmatize
    :return: List of words lemmatized
    """
    text = nlp(text)
    return ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])


# 4. Tokenization
def tokenization(text):
    """
    Italian Tokenization using NLTK Corpus and Stemmers
    Need to be applied to a single text, so at every row in a dataframe (using Apply)
    :param text: a single row with input text
    :return: processed text
    """

    # dictionary of Italian stop-words
    it_stop_words = nltk.corpus.stopwords.words('italian')
    # Snowball stemmer with rules for the Italian language
    ita_stemmer = nltk.stem.snowball.ItalianStemmer(ignore_stopwords=True)
    tokens = nltk.word_tokenize(text)

    # Tokenize
    tokens = [token.strip() for token in tokens]

    # Remove stop words
    tokens = [token for token in tokens if token not in it_stop_words]

    # Stem
    tokens = [ita_stemmer.stem(token) for token in tokens]

    # Reconstruct the text
    token_result = ' '.join([token for token in tokens])

    return token_result

# 7. Term frequency (for wordcloud) (Key terms)
# Count number of words:
# https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0

# 8. Wordcloud
# https://towardsdatascience.com/creating-word-clouds-with-python-f2077c8de5cc
# https://github.com/kaparker/gameofthrones-wordclouds/blob/master/gotwordcloud.py#L121

# 9. Sentiment
# https://towardsdatascience.com/sentiment-analysis-with-python-part-1-5ce197074184
# https://towardsdatascience.com/creating-the-twitter-sentiment-analysis-program-in-python-with-naive-bayes-classification-672e5589a7ed
# https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
# Libreria consigliata da cez
# https://polyglot.readthedocs.io/en/latest/Sentiment.html
# https://polyglot.readthedocs.io/en/latest/Sentiment.html

# 10. Word2Vec Model
# https://towardsdatascience.com/word2vec-from-scratch-with-numpy-8786ddd49e72
# https://towardsdatascience.com/a-beginners-guide-to-word-embedding-with-gensim-word2vec-model-5970fa56cc92
# https://stackabuse.com/implementing-word2vec-with-gensim-library-in-python/

# 11. Confronto tra periodi diversi

# 12 TFIDF Python
# https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089
# https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
