from gensim.models.word2vec import Word2Vec
from collections import Counter
import os
from glob import glob
from zipfile import ZipFile
import sys  
import _pickle as pickle
all_sentences=[]



list_of_dirs = os.listdir('/scratch/bsg348-share/MLCS/data-new/clean_Mar_20')
for directory in list_of_dirs:
	if not directory.endswith('zip') and not directory.startswith('.'):
		files=os.listdir('/scratch/bsg348-share/MLCS/data-new/clean_Mar_20/'+directory+'/maj')
		print(directory)
		for file_name in files:
			new_file_name='/scratch/bsg348-share/MLCS/data-new/clean_Mar_20/'+directory+'/maj/'+file_name
			with open(new_file_name, mode='rb') as f_obj:
  				test = pickle.load(f_obj)
  				for para in test:
  					para=para.strip()
  					texts = [w for w in para.lower().split(" ")]
  					all_sentences.append(texts)
  				


print('training word2vec started')
#training word2vec, size=the final word2vec length, min_count= the threshold count below which words should be ignored, worker= parallel training
model = Word2Vec(all_sentences, size=100, window=5, min_count=5, workers=4)
model.save("word2vec_model_cleaned_data")

'''
Usage:
model=Word2Vec.load('word2vec_model_cleaned_data')
model.similarity('man','woman')
'''
