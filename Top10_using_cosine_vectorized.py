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
word2Vec_dimension = 100
data_dir = 'data'
case_dir = os.path.join(data_dir, 'clean_Mar_20')
maj_dir = 'maj'
thermometer_vectors = np.zeros((len(thermometers), word2Vec_dimension))
i = 0
for thermometer in thermometers:
    words = thermometer.split()
    word2vector = np.zeros(word2Vec_dimension)
    for word in words:
        word2vector += model.wv[word]
    thermometer_vectors[i, :] = word2vector / len(words)
    i += 1
Top10words = [[0 for x in range(40)] for y in range(10)]
Top10Similarities = np.zeros((10,40))

norm_thermometer = np.linalg.norm(thermometer_vectors, axis=1)
normalized_thermometer_vectors = (np.true_divide(thermometer_vectors, norm_thermometer[:, None]))
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
            words = para.split()
            symbols = '${}()[].,:;+-*/&|<>=~" '
            words = map(lambda element: element.translate(
                {ord(c): None for c in symbols}).strip(), words)
            words = [x.lower() for x in words if x]
            for word in words:
                try:
                    word2vector = model.wv[word]
                    word2vector = word2vector/(np.linalg.norm(word2vector))
                    similarities = np.dot(normalized_thermometer_vectors,word2vector); # 1*40 array
                    idx = similarities.index(max(similarities));
                    idx_t = Top10Similarities[:,idx].index(min(Top10Similarities[:,idx]));
                    if(similarities[idx] > Top10Similarities[idx_t,idx]):
                        Top10Similarities[:,idx_t] = similarities[idx];
                        Top10words[idx_t][idx] = word;
                except:
                    pass
            print(Top10Similarities);
            print(Top10words);
