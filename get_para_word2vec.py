from gensim.models.word2vec import Word2Vec
import os
from glob import glob
from zipfile import ZipFile
import sys
import pickle
import numpy as np

# reload(sys)
# sys.setdefaultencoding('utf8')
model = Word2Vec.load('word2vec_model_cleaned_data')
thermometeres = ['democrats', 'republicans', 'protestants', 'catholics', 'jews', 'blacks', 'whites', 'southerners',
                 'big business', 'labor unions', 'liberals', 'conservatives', 'military', 'policemen',
                 'black militants', 'civil rights leaders', 'chicanos hispanics', 'democratic party',
                 'middle class people', 'people on welfare', 'political independents', 'political parties',
                 'poor people', 'republican party', 'womens right activist', 'young people', 'asian-americans', 'congress',
                 'environmentalists', 'anti abortionists', 'federal government', 'illegal aliens',
                 'christian fundamentalists', 'radical students', 'farmers', 'feminists', 'evangelical groups',
                 'elderly', 'supreme court', 'women']
all_w2v = {}
list_of_dirs = os.listdir('/scratch/bsg348-share/MLCS/data/clean_Mar_20')
for directory in list_of_dirs:
    if not directory.endswith('zip'):
        files = os.listdir('/scratch/bsg348-share/MLCS/data/clean_Mar_20/' + directory + '/maj')
        print(directory)
        for file_name in files:
            new_file_name = '/scratch/bsg348-share/MLCS/data/clean_Mar_20/' + directory + '/maj/' + file_name
            therm_param = []
            with open(new_file_name, mode='rb') as f_obj:
                test = pickle.load(f_obj)
                current_file_therm_para=[]
                for para in test:
                    words = para.split()
                    therm_param = np.zeros(len(thermometeres))
                    for word in words:
                        word=word.lower()
                        for index in range(len(thermometeres)):
                            therm_word = thermometeres[index]
                            split_therm=therm_word.split()
                            current_similarity=0
                            for ind_therm_param in split_therm:
                                try:
                                    current_similarity+=model.similarity(word,ind_therm_param)
                                except:
                                    pass

                            therm_param[index]=therm_param[index]+current_similarity/len(split_therm)
                    therm_param/=len(words)
                    current_file_therm_para.append(therm_param)
                all_w2v[new_file_name]=current_file_therm_para

pickle.dump( all_w2v, open( "para_similarity.p", "wb" ) )



# output_para_word_vec.append(current_file_word_vec)






