import os
import pickle

root_dir = 'data/clean_Mar_20'

def updateRootDir(val):
    global root_dir
    root_dir = val

def getDirectoryList(root_Directory):
    updateRootDir(root_Directory)
    return  os.listdir(root_Directory)

def getFilesListFromDir(directory):
    return os.listdir(root_dir +"/" +directory + '/maj')

def createDirectory(directory_loc):
    if not os.path.exists(directory_loc):
        os.makedirs(directory_loc)

def getParaListFromFile(file_name, directory):
    new_file_name = root_dir + "/" + directory + '/maj/' + file_name
    with open(new_file_name, mode='rb') as f_obj:
        return pickle.load(f_obj)

def writeToPickle(list, parentDir, directory, file_name, avg):
    if(avg == True):
        pickle.dump(list, open( parentDir + "/" + directory + "/" + "Avg" + file_name, "wb"))
    else:
        pickle.dump(list, open( parentDir + "/" + directory + "/" + file_name, "wb"))