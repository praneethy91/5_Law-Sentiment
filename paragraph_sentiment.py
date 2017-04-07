# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:14:22 2017

@author: naman

To start the server:
java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

timeout can be changed


"""

from pycorenlp import StanfordCoreNLP
import pickle
import os

#all_paraSent = {}
list_of_dirs = os.listdir('/scratch/bsg348-share/MLCS/data/clean_Mar_20')
for directory in list_of_dirs:
    if not directory.endswith('zip'):
        files = os.listdir('/scratch/bsg348-share/MLCS/data/clean_Mar_20/' + directory + '/maj')
        print(directory)
        if not os.path.exists("sentiment"):
            os.makedirs("sentiment")
            if not os.path.exists("sentiment/" + directory):
                os.makedirs("sentiment/" + directory)
        for file_name in files:
            new_file_name = '/scratch/bsg348-share/MLCS/data/clean_Mar_20/' + directory + '/maj/' + file_name
            with open(new_file_name, mode='rb') as f_obj:
                para_list = pickle.load(f_obj)
                '''
                para_list = [
                    "Several cities, New York City in particular for this paper, have a 311 24-hour hot line and online service, which allows anyone, residents and tourists, to report a non-emergency problem. Reported 311 problems are passed along to government services, who address and solve the problem. The records of 311 calls are publicly open and updated daily.",
                    "Analysis of 311 calls can clearly be of great use for a wide variety of purposes, ranging from a rich understanding of the status of a city to the effectiveness of the government services in addressing such calls. Ideally, the analysis can also support a prediction of future 311 calls, which would enable the assignment of service resources by the city government.",
                    "We have been extensively analyzing 311 calls in NYC. In this paper, we profile the data set and highlight a few interesting facts. We provide statistics along complaint types, geolocation, and temporal patterns and show the diversity of the big 311 data along those dimensions. We then discuss the prediction problem of number of calls, where we experiment with different sets of semantic features. We show that the prediction error for different complaint types can significantly vary if some features are not considered."]
                '''
                nlp = StanfordCoreNLP('http://localhost:9000')
                curr_file_allPara_sent = []
                for para in para_list:
                    res = nlp.annotate(para,
                                       properties={
                                           'annotators': 'sentiment',
                                           'outputFormat': 'json',
                                            'timeout': 1000,
                                        })
                    para_sentiment = 0
                    for s in res["sentences"]:
                        '''
                        print("%d: '%s': %s %s" % (
                            s["index"],
                            " ".join([t["word"] for t in s["tokens"]]),
                            s["sentimentValue"], s["sentiment"]))
                        '''
                        sentimentVal = s["sentimentValue"]
                        para_sentiment += int(sentimentVal) - 2
                    sentiment = 1 if para_sentiment > 0 else -1
                    curr_file_allPara_sent.append(sentiment)
                    '''
                    print(sentiment)
                    '''
                pickle.dump(curr_file_allPara_sent, open("sentiment/" + directory + "/" + file_name, "wb"))
                #all_paraSent[new_file_name] = curr_file_allPara_sent

#pickle.dump( all_paraSent, open( "para_sentiment.p", "wb" ) )