import os
import pickle

def getDirectoryList(root_Directory):
    return  os.listdir(root_Directory)

def getFilesListFromDir(directory):
    return os.listdir('data/clean_Mar_20/' + directory + '/maj')

def createDirectory(directory_loc):
    if not os.path.exists(directory_loc):
        os.makedirs(directory_loc)

def getParaListFromFile(file_name, directory):
    new_file_name = 'data/clean_Mar_20/' + directory + '/maj/' + file_name
    with open(new_file_name, mode='rb') as f_obj:
        return pickle.load(f_obj)

def writeToPickle(list, directory, file_name, avg):
    if(avg == True):
        pickle.dump(list, open("sentiment/" + directory + "/" + file_name + "-avg", "wb"))
    else:
        pickle.dump(list, open("sentiment/" + directory + "/" + file_name, "wb"))
