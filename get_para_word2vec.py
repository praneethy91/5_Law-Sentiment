import os
import pickle
import utils
import numpy as np
from gensim.models.word2vec import Word2Vec

model = Word2Vec.load('w2vmodel_run/word2vec_model_cleaned_data')
thermometers = ['democrats', 'republicans', 'protestants', 'catholics', 'jews', 'blacks', 'whites', 'southerners',
                'big business', 'labor unions', 'liberals', 'conservatives', 'military', 'policemen',
                'black militants', 'civil rights leaders', 'chicanos hispanics', 'democratic party',
                'middle class people', 'people on welfare', 'political independents', 'political parties',
                'poor people', 'republican party', 'women right activist', 'young people', 'asian americans',
                'congress',
                'environmentalists', 'anti abortionists', 'federal government', 'illegal aliens',
                'christian fundamentalists', 'radical students', 'farmers', 'feminists', 'evangelical groups',
                'elderly', 'supreme court', 'women']

# Word2Vec size
word2Vec_dimension = 100

# Data directory for cases
data_dir = 'data'
case_dir = os.path.join(data_dir, 'clean_Mar_20')

# sub-directory containing our cases
maj_dir = 'maj'

# similarities output directory
similarities_output_dir = "/home/bsg348/similarities"

# Converting thermometers to vectors
thermometer_vectors = np.zeros((len(thermometers), word2Vec_dimension))
i = 0
for thermometer in thermometers:
    words = thermometer.split()
    word2vector = np.zeros(word2Vec_dimension)
    for word in words:
        word2vector += model.wv[word]
    thermometer_vectors[i, :] = word2vector / len(words)
    i += 1

list_of_dirs = [d for d in os.listdir(case_dir) if os.path.isdir(os.path.join(case_dir, d))]

for directory in list_of_dirs:
    print(directory)
    files = os.listdir(os.path.join(case_dir, directory, maj_dir))
    utils.createDirectory(os.path.join(similarities_output_dir, directory))
    for file_name in files:
        absolute_file_path = os.path.join(case_dir, directory, maj_dir, file_name)
        therm_param = []
        with open(absolute_file_path, mode='rb') as f_obj:
            para_list = pickle.load(f_obj)
        current_file_therm_para = []
        for para in para_list:

            # Filtering the word list in the para and removing all special symbols
            words = para.split()
            symbols = '${}()[].,:;+-*/&|<>=~" '
            words = map(lambda element: element.translate(
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

            # removing the last rows of 0's and checking for actual length
            if actual_len != 0:
                arr = arr[0:actual_len, :]
            else:
                arr = np.zeros((1, word2Vec_dimension))
                actual_len = 1

            # Calculating norms of the thermometer vector and the para vectors
            norm_arr = np.linalg.norm(arr, axis=1)
            norm_thermometer = np.linalg.norm(thermometer_vectors, axis=1)

            # Multiplying to get similarities
            with np.errstate(divide='ignore', invalid='ignore'):

                normalized_arr = np.true_divide(arr, norm_arr[:, None])
                normalized_thermometer_vectors = (np.true_divide(thermometer_vectors, norm_thermometer[:, None]))

                normalized_arr[~ np.isfinite(normalized_arr)] = 0
                normalized_thermometer_vectors[~ np.isfinite(normalized_thermometer_vectors)] = 0

                similarity_vector = np.dot(normalized_arr, normalized_thermometer_vectors.T)
                similarity_vector = np.sum(similarity_vector, axis=0) / actual_len

                current_file_therm_para.append(similarity_vector)

        pickle.dump(current_file_therm_para, open(os.path.join(similarities_output_dir, directory, file_name), "wb"))