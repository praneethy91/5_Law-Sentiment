from gensim.models.word2vec import Word2Vec
from collections import Counter
import os
from glob import glob
from zipfile import ZipFile
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
list_of_dirs = os.listdir('/scratch/bsg348-share/MLCS')
all_sentences=[]



zipfiles = glob('/scratch/bsg348-share/MLCS/data/*zip')

for zfname in zipfiles:#loading all zipfiles in the data directory

    zfile = ZipFile(zfname)
    year = zfname.split('/')[-1][:-4]

    members = zfile.namelist()
    threshold = len(members) / 200
    docfreqs = Counter()

    for fname in members:#files in zipfile
        if not fname.endswith('-maj.txt'):#use only the file that ends with maj.txt
            continue

        docid = fname.split('/')[-1][:-4]
        text = zfile.open(fname).read().decode()
        stoplist = set(["for", "a", "of", "the", "and", "to", "in", "J.", "j.", "d.", "D.", "."])
        data = text.replace('\r', '').replace('\n', '').strip()  # replace('\n', " ")
        texts = [word for word in data.lower().split(" ") if word not in stoplist]#representing text as a list of words
        all_sentences.append(texts)# appending current list to original list of list of words


#training word2vec, size=the depth of nnlayers, min_count= the threshold count below which words should be ignored, worker= parallel training
model = Word2Vec(all_sentences, size=100, window=5, min_count=5, workers=4)
model.save("word2vec_model")

'''
Usage:
model=Word2Vec.load('word2vec_model')
model.wv.similarity('man','woman')
'''