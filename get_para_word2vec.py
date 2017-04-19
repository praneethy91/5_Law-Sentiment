import os
import pickle

import numpy as np
import time
from gensim.models.word2vec import Word2Vec

# reload(sys)
# sys.setdefaultencoding('utf8')

model = Word2Vec.load('w2vmodel_run/word2vec_model_cleaned_data')
thermometeres = ['democrats', 'republicans', 'protestants', 'catholics', 'jews', 'blacks', 'whites', 'southerners',
                 'big business', 'labor unions', 'liberals', 'conservatives', 'military', 'policemen',
                 'black militants', 'civil rights leaders', 'chicanos hispanics', 'democratic party',
                 'middle class people', 'people on welfare', 'political independents', 'political parties',
                 'poor people', 'republican party', 'womens right activist', 'young people', 'asian-americans', 'congress',
                 'environmentalists', 'anti abortionists', 'federal government', 'illegal aliens',
                 'christian fundamentalists', 'radical students', 'farmers', 'feminists', 'evangelical groups',
                 'elderly', 'supreme court', 'women']

# Wrod2Vec size
word2Vec_dimension = 100

# Converting thermometers to vectors

thermometer_vectors = np.zeros((len(thermometeres), word2Vec_dimension))
i = 0
for thermometer in thermometeres:
    words = thermometer.split()
    word2vector = np.zeros(word2Vec_dimension)
    for word in words:
        word2vector += model.wv[word]
    thermometer_vectors[i, :] = word2vector/len(words)
    i += 1

start_time = time.time()
list_of_dirs = os.listdir('data/clean_Mar_20')
for directory in list_of_dirs:
    if not directory.endswith('zip'):
        files = ['data/clean_Mar_20/1964_new/maj/X2NCO1-maj.p']
        print(directory)
        os.makedirs("similarities/"+directory, exist_ok=True)
        for file_name in files:
            new_file_name = file_name
            therm_param = []
            with open(new_file_name, mode='rb') as f_obj:
                para_list = pickle.load(f_obj)
                current_file_therm_para=[]
                for para in para_list:

                    # Filtering the word list in the para and removing all special symbols
                    words = para.split()
                    symbols = '${}()[].,:;+-*/&|<>=~" '
                    words = map(lambda Element: Element.translate(
                        {ord(c): None for c in symbols}).strip(), words)
                    words = [x.lower() for x in words if x]

                    arr = np.zeros((len(words), word2Vec_dimension))
                    i = 0
                    actual_len = 0
                    for word in words:
                        try:
                            word2vector = model.wv[word]
                            arr[actual_len, :] = word2vector
                            actual_len += 1
                        except:
                            pass

                    # removing the last rows of 0's
                    arr = arr[0:actual_len, :]

                    # Calculating norms of the thermometer vector and the para vectors
                    norm_arr = np.linalg.norm(arr, axis=1)
                    norm_thermometer = np.linalg.norm(thermometer_vectors, axis=1)

                    # Multiplying to get similarities
                    similarity_vector = np.dot(np.true_divide(arr, norm_arr[:, None])
                                               , (np.true_divide(thermometer_vectors, norm_thermometer[:, None])).T)

                    similarity_vector = np.sum(similarity_vector, axis=0)/actual_len

                    current_file_therm_para.append(similarity_vector)

                pickle.dump(current_file_therm_para, open( "similarities/"+directory+"/"+'X2NCO1-maj', "wb" ) )

end_time = time.time()
print(end_time - start_time)



#pickle.dump( all_w2v, open( "para_similarity.p", "wb" ) )
# output_para_word_vec.append(current_file_word_vec)






