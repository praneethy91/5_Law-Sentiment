# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 13:14:22 2017

@author: naman

To start the server:
java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

timeout can be changed


"""
from gensim.models.word2vec import Word2Vec
import numpy as np
from pycorenlp import StanfordCoreNLP
import pickle
import os

model = Word2Vec.load('w2vmodel_run/word2vec_model_cleaned_data')
thermometeres = ['democrats', 'republicans', 'protestants', 'catholics', 'jews', 'blacks', 'whites', 'southerners',
                 'big business', 'labor unions', 'liberals', 'conservatives', 'military', 'policemen',
                 'black militants', 'civil rights leaders', 'chicanos hispanics', 'democratic party',
                 'middle class people', 'people on welfare', 'political independents', 'political parties',
                 'poor people', 'republican party', 'womens right activist', 'young people', 'asian-americans', 'congress',
                 'environmentalists', 'anti abortionists', 'federal government', 'illegal aliens',
                 'christian fundamentalists', 'radical students', 'farmers', 'feminists', 'evangelical groups',
                 'elderly', 'supreme court', 'women']


list_of_dirs = os.listdir('/scratch/bsg348-share/MLCS/data/clean_Mar_20')
for directory in list_of_dirs:
    if not directory.endswith('zip'):
        files = os.listdir('/scratch/bsg348-share/MLCS/data/clean_Mar_20/' + directory + '/maj')
        print(directory)
        if not os.path.exists("mixed"):
            os.makedirs("mixed")
            if not os.path.exists("mixed/" + directory):
                os.makedirs("mixed/" + directory)
        for file_name in files:
            new_file_name = '/scratch/bsg348-share/MLCS/data/clean_Mar_20/' + directory + '/maj/' + file_name
            therm_param = []
            with open(new_file_name, mode='rb') as f_obj:
                para_list = pickle.load(f_obj)
                nlp = StanfordCoreNLP('http://localhost:9000')
                curr_file_allPara_ss = []
                for para in para_list:
                    #Sentiment for paragraph - BEGIN
                    res = nlp.annotate(para,
                                       properties={
                                           'annotators': 'sentiment',
                                           'outputFormat': 'json',
                                            'timeout': 1000,
                                        })
                    para_sentiment = 0
                    for s in res["sentences"]:
                        sentimentVal = s["sentimentValue"]
                        para_sentiment += int(sentimentVal) - 2
                    sentiment = 1 if para_sentiment > 0 else -1

                    #Sentime for paragraph -END

                    #Similarity Score for Paragraph - Begin
                    words = para.split()
                    therm_param = np.zeros(len(thermometeres))
                    for word in words:
                        word = word.lower()
                        for index in range(len(thermometeres)):
                            therm_word = thermometeres[index]
                            split_therm = therm_word.split()
                            current_similarity = 0
                            for ind_therm_param in split_therm:
                                try:
                                    current_similarity += model.similarity(word, ind_therm_param)
                                except:
                                    pass

                            therm_param[index] = therm_param[index] + current_similarity / len(split_therm)

                    therm_param = (sentiment * therm_param)/len(words)
                    # Similarity score for paragraph - END

                    curr_file_allPara_ss.append(therm_param)
                pickle.dump(curr_file_allPara_ss, open("mixed/" + directory + "/" + file_name, "wb"))