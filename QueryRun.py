from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import string

users_tf_list = list()  # tf of every word in the query


class QueryRun:

    def __init__(self, query):
        print(" ")

    # preprocess the words the user gives as follows
    @staticmethod
    def preprocess(text):

        text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
        text = re.sub(r'[^\w]', ' ', text)  # remove rest symbols that are not punctuations
        text = re.sub(r'\d+', '', text)  # remove numbers
        text = re.sub(r'[^\x00-\x7f]', r'', text)  # keep only latin characters
        text = text.lower()  # all letters lowercase

        # remove stopwords
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)

        text = [w for w in word_tokens if not w in stop_words]
        text = []
        for w in word_tokens:
            if w not in stop_words:
                text.append(w)

        # Lemmatization(root of the word)
        lemmatizer = WordNetLemmatizer()
        for counter, word in enumerate(text):
            text[counter] = lemmatizer.lemmatize(word)

        text = list(set(text))
        text.sort()  # sort the words alphabetically

        return text

    #  calculate and save the tf of every preprocessed word of the query
    @staticmethod
    def users_tf(size_of_search):
        for i in range(size_of_search):
            users_tf_list.append(1 / size_of_search)
