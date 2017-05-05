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
list_of_dirs = [d for d in os.listdir(case_dir) if os.path.isdir(os.path.join(case_dir, d))]
for thermometer in thermometers:
    words_therm = thermometer.split()
    for word_t in words_therm:
        Top10words = [];
        Top10Similarities = [0] * 10
        for directory in list_of_dirs:
            print(directory)
            files = os.listdir(os.path.join(case_dir, directory, maj_dir))
            for file_name in files:
                absolute_file_path = os.path.join(case_dir, directory, maj_dir, file_name)
                with open(absolute_file_path, mode='rb') as f_obj:
                    para_list = pickle.load(f_obj)
                current_file_therm_para = []
                for para in para_list:
                    words = para.split()
                    symbols = '${}()[].,:;+-*/&|<>=~" '
                    words = map(lambda element: element.translate(
                        {ord(c): None for c in symbols}).strip(), words)
                    words = [x.lower() for x in words if x]
                    arr = np.zeros((len(words), word2Vec_dimension))
                    for word in words:
                        try:
                            word_sim = 0;
                            word_sim += model.similarity[word_t,word]
                            r = word_sim/(len(words_therm))
                            if(r > np.min(Top10Similarities)):
                                idx = Top10Similarities.index(min(Top10Similarities));
                                Top10Similarities[idx] = r;
                                Top10words[idx] = word;
                        except:
                            pass

        print(Top10Similarities);
        print(Top10words);                    
