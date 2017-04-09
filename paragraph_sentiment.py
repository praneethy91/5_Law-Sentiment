# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:14:22 2017

@author: naman

To start the server:
java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

timeout can be changed
"""

from pycorenlp import StanfordCoreNLP
import utils as util



def getNLPServer():
    return StanfordCoreNLP('http://localhost:9000')


def setAnnotatorsPropertiesToNLP(nlp, para):
    return nlp.annotate(para,
                       properties={
                           'annotators': 'sentiment',
                           'outputFormat': 'json',
                           'timeout': 1000,
                       })


def printSentenceResult(s):
    print("%d: '%s': %s %s" % (
        s["index"],
        " ".join([t["word"] for t in s["tokens"]]),
        s["sentimentValue"], s["sentiment"]))


def getParaSentimentList(para_list):
    nlp = getNLPServer()
    avgParaSentimentList = []
    paraSentimentList = []
    for para in para_list:
        res = setAnnotatorsPropertiesToNLP(nlp,para)
        para_sentiment = 0
        sentence_count = 0
        for s in res["sentences"]:
            #printSentenceResult(s)
            sentence_sentiment = s["sentimentValue"]
            para_sentiment += int(sentence_sentiment) - 2
            sentence_count += 1

        avgParaSentimentList.append(para_sentiment)
        sentiment = 1 if para_sentiment > 0 else (-1 if para_sentiment < 0 else 0)
        paraSentimentList.append(sentiment)
        '''
        print(sentiment)
        '''
        return avgParaSentimentList, paraSentimentList


def main():
    root_Directory = 'data/clean_Mar_20'
    list_of_dirs = util.getDirectoryList(root_Directory)
    for directory in list_of_dirs:
        if not directory.endswith('zip'):

            print(directory)
            util.createDirectory("sentiment")
            util.createDirectory("sentiment/" + directory)

            files = util.getFilesListFromDir(directory)
            for file_name in files:
                para_list = util.getParaListFromFile(file_name, directory)

                # Example para list
                '''
                para_list = [
                    "Several cities, New York City in particular for this paper, have a 311 24-hour hot line and online service, which allows anyone, residents and tourists, to report a non-emergency problem. Reported 311 problems are passed along to government services, who address and solve the problem. The records of 311 calls are publicly open and updated daily.",
                    "Analysis of 311 calls can clearly be of great use for a wide variety of purposes, ranging from a rich understanding of the status of a city to the effectiveness of the government services in addressing such calls. Ideally, the analysis can also support a prediction of future 311 calls, which would enable the assignment of service resources by the city government.",
                    "We have been extensively analyzing 311 calls in NYC. In this paper, we profile the data set and highlight a few interesting facts. We provide statistics along complaint types, geolocation, and temporal patterns and show the diversity of the big 311 data along those dimensions. We then discuss the prediction problem of number of calls, where we experiment with different sets of semantic features. We show that the prediction error for different complaint types can significantly vary if some features are not considered."]
                '''

                avgParaSentimentList, paraSentimentList = getParaSentimentList(para_list)
                util.writeToPickle(paraSentimentList, directory, file_name, avg=False)
                util.writeToPickle(avgParaSentimentList, directory, file_name, avg=True)

if __name__ == "__main__":
    main()