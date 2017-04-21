import os
import pickle

root_dir = 'data/clean_Mar_20'

def updateRootDir(val):
    global root_dir
    root_dir = val

def getDirectoryList(root_Directory):
    #print(root_dir)
    updateRootDir(root_Directory)
    #print(root_dir)
    return  os.listdir(root_Directory)

def getFilesListFromDir(directory, orignal = True):
    maj = ''
    if(orignal):
        maj = '/maj'
    return os.listdir(root_dir +"/" +directory + maj)

def createDirectory(directory_loc):
    if not os.path.exists(directory_loc):
        os.makedirs(directory_loc)

def getParaListFromFile(file_name, directory):
    new_file_name = root_dir + "/" + directory + '/maj/' + file_name
    return getDataFromPickle(new_file_name)

def getDataFromPickle(file, directory = ''):
    with open(directory + file, mode='rb') as f_obj:
        return pickle.load(f_obj)

def writeToPickle(list, parentDir, directory, file_name, avg=False):
    if(avg == True):
        pickle.dump(list, open( parentDir + "/" + directory + "/" + "Avg" + file_name, "wb"))
    else:
        pickle.dump(list, open( parentDir + "/" + directory + "/" + file_name, "wb"))
