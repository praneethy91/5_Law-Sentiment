import os
import pickle
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
#data_dir = 'data'
#case_dir = os.path.join(data_dir, 'clean_Mar_20')
case_dir = '/scratch/bsg348-share/MLCS/data/clean_Mar_20'
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
Top10words = [[0 for x in range(10)] for y in range(40)]
Top10Similarities = [[0 for x in range(10)] for y in range(40)]
num = [0 for x in range(65)];
norm_thermometer = np.linalg.norm(thermometer_vectors, axis=1)
normalized_thermometer_vectors = (np.true_divide(thermometer_vectors, norm_thermometer[:, None]))
list_of_dirs = [d for d in os.listdir(case_dir) if os.path.isdir(os.path.join(case_dir, d))]
i = 1;
for directory in list_of_dirs:
    num[0] = num[0] +1;
    num[i] = directory;
    i = i +1;
    print(directory)
    files = os.listdir(os.path.join(case_dir, directory, maj_dir))
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
                    similarities = similarities.tolist()
                    idx = similarities.index(max(similarities));
                    sim_list = Top10Similarities[idx] # list of 10 elements
                    idx_t = sim_list.index(min(sim_list));
                    if(similarities[idx] > Top10Similarities[idx][idx_t] and not(word in Top10words[idx]) and not(word in thermometers)):
                        Top10Similarities[idx][idx_t] = similarities[idx];
                        Top10words[idx][idx_t] = word;
                except:
                    pass
    print(Top10Similarities);
    with open('outfile_w_2', 'wb') as fp:
        pickle.dump(Top10words, fp)
    with open('outfile_s_2', 'wb') as fp:
        pickle.dump(Top10Similarities, fp)
    print(Top10words);
    with open('outfile_num', 'wb') as fp:
        pickle.dump(num, fp)
    '''
    with open ('outfile', 'rb') as fp:
        itemlist = pickle.load(fp)
    '''
i = 0;
temp = []
for X in Top10words:
  Y = Top10Similarities[i]
  temp.append([x for (y,x) in sorted(zip(Y,X))])
  i = i + 1;
result = []
for X in temp:
    T = [i for i in reversed(X)]
    result.append(T)
print(result)
sim = [];
for X in Top10Similarities:
    sim.append(sorted(X,reverse=True))
