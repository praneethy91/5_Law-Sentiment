
import phrase_tokenizer.py

root_Directory = 'data/clean_Mar_20'
list_of_dirs = utils.getDirectoryList(root_Directory)

# Training the phraser
phrase2id, id2phrase = train_phraser()

# Phrase vector of the thermometers
thermometer_vector = [phrase_similarity.PhraseVector(thermometer) for thermometer in thermometers]

# Getting data from the phraser
for directory in list_of_dirs:
    if not directory.endswith('zip'):
        utils.createDirectory("similarities2")
        utils.createDirectory("similarities2/" + directory)
        
        files = utils.getFilesListFromDir(directory)
        for file_name in files:
            print(file_name)
            para_list = utils.getParaListFromFile(file_name, directory)
            print(para_list)
            print('in year')
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
            utils.writeToPickle(caseLevelParaSimilarityVectorsCombined,"similarities2",directory,file_name,False)
            #pickle.dump(caseLevelParaSimilarityVectorsCombined, open("similarities/" + directory + "/" + file_name, "wb"))
            print('dumped into',file_name)
