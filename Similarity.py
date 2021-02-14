import pandas as pd
import csv
import math


class Similarity:
    idf = list()  # a list that keeps the idf from every url that contains any word of the query
    tf = list()  # a list that keeps the tf from every url that contains any word of the query
    urls = list()  # a list that keeps all the urls that contains any word of the query
    weight_of_url = list()  # a list that keeps the idf*tf for every url that contains any word of the query and the url
    result_urls = list()  # the urls that we will return to the user

    def __init__(self, search, query_tf, topK):
        self.copy_index()
        self.tf_idf(search)
        self.cosine_similarity(query_tf, topK)
        #  we clear all the lists for every different query
        Similarity.idf.clear()
        Similarity.tf.clear()
        Similarity.urls.clear()
        Similarity.weight_of_url.clear()

    @staticmethod
    def copy_index():
        # we copy the inverted index a new csv, so when we crawl we have the previous index until the crawl gets done
        df = pd.read_csv('Inverted Index.csv', error_bad_lines=False)
        df.to_csv('copy of Inverted Index.csv', header=True, index=False)

    @staticmethod
    def tf_idf(list_search):
        file = open('copy of Inverted Index.csv', 'r')
        reader = csv.reader(file)  # read the contents of the index

        # initialize all lists with '0' or " " and create sublists where is needed
        for i in range(len(list_search)):
            Similarity.idf.append(0)
            Similarity.tf.append(0)
            Similarity.urls.append("")
            Similarity.weight_of_url.append("")
            Similarity.tf[i] = list()
            Similarity.tf[i].append(0)
            Similarity.urls[i] = list()
            Similarity.urls[i].append("")
            Similarity.weight_of_url[i] = list()
            Similarity.weight_of_url[i].append("")
        for row in reader:  # for every word in the index
            for word in list_search:  # and for every word from query
                if word == row[0]:  # search if they match
                    result = row[1]  # keep the infos from match urls, frequency, number of words that the url contains)
                    result = result.replace("[", "")
                    result = result.replace("]", "")
                    result = result.split(",")
                    contains_word = len(result)/3  # number of urls that contain the word
                    f = open("numOfSites.txt", "r")
                    num_of_sites = int(f.read())  # read from a file the number of sites that got crawled the last time
                    Similarity.idf[list_search.index(word)] = math.log10(num_of_sites/contains_word)  # word's idf
                    Similarity.tf[list_search.index(word)] = list()
                    Similarity.urls[list_search.index(word)] = list()
                    Similarity.weight_of_url[list_search.index(word)] = list()
                    for j in range(int(contains_word)):  # scan every url contains the word
                        step = 3*j  # this step just check the frequency and skip rest infos
                        Similarity.tf[list_search.index(word)].append(int(result[step])/int(result[2 + step]))  # for
                        # every word in the tf list we create a sublist that contains the tf for every different url
                        Similarity.urls[list_search.index(word)].append(result[step + 1])  # save the url in the list

    @staticmethod
    def cosine_similarity(query_tf, top_k):
        Similarity.result_urls.clear()
        # users_tf_idf = list()
        distinct_urls = list()  # every distinct url
        print_urls = list()  # the urls that we will return
        for i in range(len(Similarity.tf)):  # for every word
            # users_tf_idf.append(query_tf[i]*Similarity.idf[i])
            for j in range(len(Similarity.tf[i])):  # calculate the weight of every url that contains the word(sublist)
                Similarity.tf[i][j] = Similarity.tf[i][j]*Similarity.idf[i]  # with tf*idf
        for i in range(len(Similarity.tf)):
            for j in range(len(Similarity.tf[i])):
                if Similarity.tf[i][j] != 0:  # if the weight isnt 0
                    # for every distinct url
                    Similarity.weight_of_url[i].append(Similarity.tf[i][j])  # append it in the weight_of_url list
                    Similarity.weight_of_url[i].append(Similarity.urls[i][j])  # exact after append the url,
                    # so they are next each other.
                    if Similarity.urls[i][j] not in distinct_urls:
                        distinct_urls.append(Similarity.urls[i][j])  # append the distinct url

        cosines = list()  # this list will contain all cosines similarities for urls
        numerator = 0
        url_measure = 0
        query_measure = 0
        for k in range(len(distinct_urls)):
            temp_cos = list()  # here we will copy the weight_of_url list
            for i in range(len(Similarity.weight_of_url)):
                temp_cos.append(0)
            for i in range(len(Similarity.weight_of_url)):
                for j in range(len(Similarity.weight_of_url[i])):
                    if Similarity.weight_of_url[i][j] == distinct_urls[k]:  # append the distinct url match with
                        # current url of weight_of_url list
                        temp_cos[i] = Similarity.weight_of_url[i][j-1]  # append in the temp_cos list the weight
            for i in range(len(temp_cos)):  # here we calculate the cosine similarity
                numerator = numerator + temp_cos[i]*query_tf[i]  # this is the type of numerator
                url_measure = url_measure + math.pow(temp_cos[i], 2)  # this sums the urls cosines similarities squared
                query_measure = query_measure + math.pow(query_tf[i], 2)   # this sums users tf squared
            url_measure = math.sqrt(url_measure)  # this is ||url_measure||
            query_measure = math.sqrt(query_measure)  # this is ||query_measure||
            type_of_cos = numerator/(url_measure*query_measure)  # save the result of cosine similarity
            cosines.append(type_of_cos)  # append it
        for k in range(top_k):  # depends in the top K documents the user will ask for
            if not cosines:
                break
            index = cosines.index(max(cosines))  # the url with the biggest cosine similarity
            print_urls.append(distinct_urls[index])  # save this url
            cosines.pop(index)  # then delete it so in the next loop we save the next max
            distinct_urls.pop(index)  # delete also from the distinct_urls, so we wont scan it again
        Similarity.result_urls = print_urls  # return the urls as result
