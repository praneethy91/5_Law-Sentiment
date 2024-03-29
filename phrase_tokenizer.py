# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 12:06:40 2016

@author: elliott
"""

from numpy import prod
from collections import Counter, Set
from nltk import sent_tokenize,ngrams,PorterStemmer,SnowballStemmer,WordNetLemmatizer
from nltk.tag import perceptron
import utils
import phrase_similarity
import numpy as np
import pickle

tagger = perceptron.PerceptronTagger()
porter = PorterStemmer()
snowball = SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()

thermometers = ['democrats', 'republicans', 'protestants', 'catholics', 'jews', 'blacks', 'whites', 'southerners',
                 'big business', 'labor unions', 'liberals', 'conservatives', 'military', 'policemen',
                 'black militants', 'civil rights leaders', 'chicanos hispanics', 'democratic party',
                 'middle class people', 'people on welfare', 'political independents', 'political parties',
                 'poor people', 'republican party', 'womens right activist', 'young people', 'asian-americans', 'congress',
                 'environmentalists', 'anti abortionists', 'federal government', 'illegal aliens',
                 'christian fundamentalists', 'radical students', 'farmers', 'feminists', 'evangelical groups',
                 'elderly', 'supreme court', 'women']

def word_normalize(word,stemmer=None):
    w = word.lower()
    if stemmer == 'porter':
        w = porter.stem(w)
    elif stemmer == 'snowball':
        w = snowball.stem(w)
    elif stemmer == 'lemma':
        w = lemmatizer.lemmatize(w)
    return w
    
# Normalize Penn tags
tagdict = {'NN':'N',
            'NNS':'N',
            'NNP':'N',
            'NNPS':'N',
            'JJ':'A',
            'JJR':'A',
            'JJS':'A',
            'VBG':'A',
            'RB':'A', # adverbs treated as adjectives
            'DT':'D',
            'IN':'P',
            'TO':'P',
            'VB':'V',
            'VBD':'V',
            'VBN':'V',
            'VBP':'V',
            'VBZ':'V',
            
            'MD': 'V', # modals treated as verbs
            'RP': 'V', # particles treated as verbs
            'CC': 'C'}

# Allowed sequences of tag patterns (from Ash 2016)
tagpatterns = {'A','N','J',
           'AN','NN', 'VN', 'VV', 'NV',
            'VP',                                    
            'NNN','AAN','ANN','NAN','NPN',
            'VAN','VNN', 'AVN', 'VVN',
            'VPN','ANV','NVV','VDN', 'VVV', 'NNV',
            'VVP','VAV','VVN',
            'NCN','VCV', 'ACA',  
            'PAN',
            'NCVN','ANNN','NNNN','NPNN', 'AANN' 'ANNN','ANPN','NNPN','NPAN', 
            'ACAN', 'NCNN', 'NNCN', 'ANCN', 'NCAN',
            'PDAN', 'PNPN',
            'VDNN', 'VDAN','VVDN'}

def tagsentence(sent,stemmer=None,vocab=None):
    # convert to one-letter tags if applicable, 
    # replace with none if word not in vocab
    # replace with none if tag not in tagdict
    tagwords = []
    for x in tagger.tag(sent):
        if (vocab is None or x[0] in vocab) and x[1] in tagdict:
            normword = word_normalize(x[0],stemmer=stemmer)
            normtag = tagdict[x[1]]
            tagwords.append((normword,normtag))
        else:
            tagwords.append(None)
    return tagwords

def gmean(phrase, termfreqs):
    """geometric mean association."""
    n = len(phrase)
    p = [termfreqs[w] for w in phrase.split('_')]
    pg = termfreqs[phrase]    
    return pg / (prod(p) ** (1/n))

def train_phraser(max_phrase_length=3, stemmer=None, vocab=None,
                            min_doc_freq=None, min_gmean=None):    
    # take documents and get POS-gram dictionary
    
    numdocs = 0
    docfreqs = Counter()
    termfreqs = Counter()

    root_Directory = 'data/clean_Mar_20'
    list_of_dirs = utils.getDirectoryList(root_Directory)
    for directory in list_of_dirs:
        if not directory.endswith('zip'):
            print(directory)
            utils.createDirectory("similarities")
            utils.createDirectory("similarities/" + directory)

            files = utils.getFilesListFromDir(directory)
            for file_name in files:
                para_list = utils.getParaListFromFile(file_name, directory)
                for para in para_list:

                    numdocs += 1

                    docgrams = set()
                    # split into sentences
                    sentences = sent_tokenize(para)
                    for sentence in sentences:
                        # split into words and get POS tags
                        words = sentence.split()
                        tagwords = tagsentence(words, stemmer, vocab)
                        for n in range(1, max_phrase_length + 1):
                            rawgrams = ngrams(tagwords, n)
                            for rawgram in rawgrams:
                                # skip grams that have words not in vocab
                                if None in rawgram:
                                    continue
                                gramtags = ''.join([x[1][0] for x in rawgram])
                                if gramtags in tagpatterns:
                                    # if tag sequence is allowed, add to counter
                                    gram = '_'.join([x[0] for x in rawgram])
                                    termfreqs[gram] += 1
                                    docgrams.add(gram)
                    docfreqs.update(docgrams)
        
    # filter vocabulary based on document frequency and make gram ids
    gram2id = {}
    id2gram = {}

    if min_doc_freq is None:
        min_doc_freq = round(numdocs / 200) + 1

    i = 0
    for (phrase,v) in docfreqs.most_common():   
        if v < min_doc_freq:
            break      
        if min_gmean is not None:
            # check geometric mean association
            n = v.count('_') + 1
            if len(n) >= 2:
                gscore = gmean(phrase,termfreqs) 
                if gscore[n] < min_gmean[n]:
                    continue
        gram2id[phrase] = i
        id2gram[i] = phrase
        i += 1
    
    return gram2id, id2gram

def apply_phraser(words, gram2id, max_phrase_length=3):
    """"apply phraser method to sentence."
         Input should be list of lower-case (stemmed) words"""
    sentlength = len(words)
    skip = 0
    new_s = []
    for i in range(sentlength):
        if skip > 0:
            skip -= 1
            continue
        if words[i] is None:
            continue
        for n in reversed(range(1,max_phrase_length+1)):
            if i+n > sentlength:
                continue
            gram = words[i:i+n]
            if None in gram:
                continue
            gram_word = '_'.join(gram)    
            if gram_word in gram2id:
                new_s.append(gram2id[gram_word])
                skip = n-1
                break
    return new_s

'''
documents = ['This is a test document sentence. This is the second sentence.',
         'This is a second test document.',
         'Beyond a reasonable doubt.']
'''

root_Directory = 'data/clean_Mar_20'
list_of_dirs = utils.getDirectoryList(root_Directory)

# Training the phraser
phrase2id, id2phrase = train_phraser()

# Phrase vector of the thermometers
thermometer_vector = [phrase_similarity.PhraseVector(thermometer) for thermometer in thermometers]

# Getting data from the phraser
for directory in list_of_dirs:
    if not directory.endswith('zip'):
        print(directory)
        utils.createDirectory("similarities")
        utils.createDirectory("similarities/" + directory)

        files = utils.getFilesListFromDir(directory)
        for file_name in files:
            para_list = utils.getParaListFromFile(file_name, directory)
            caseLevelParaSimilarityVectorsCombined = []
            for para in para_list:
                set_vector = set()
                sentences = sent_tokenize(para)
                for sentence in sentences:
                    # split into words and get POS tags
                    words = [w.lower() for w in sentence.split()]
                    phraseids = apply_phraser(words, phrase2id)

                    for phraseId in phraseids:
                        set_vector.add(np.array([thermometer.CosineSimilarity(phrase_similarity.PhraseVector(id2phrase[phraseId])) for thermometer in thermometer_vector]))

                paraLevelSimilarityVector = np.mean(set_vector, axis=0)
                caseLevelParaSimilarityVectorsCombined.append(paraLevelSimilarityVector)
            pickle.dump(caseLevelParaSimilarityVectorsCombined, open("similarities/" + directory + "/" + file_name, "wb"))