import os
import pickle

root_dir = 'data/clean_Mar_20'
slash = "/"

def updateRootDir(val):
    global root_dir
    root_dir = val

def getDirectoryList(root_Directory):
    updateRootDir(root_Directory)
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
    parDirSlash = slash
    dirSlash = slash
    if parentDir == '':
        parDirSlash = ""
    if dir == '': 
        dirSlash = ""
    if avg == True:
        pickle.dump(list, open( parentDir + parDirSlash + directory + dirSlash + "Avg" + file_name, "wb"))
    else:
        pickle.dump(list, open( parentDir + parDirSlash + directory + dirSlash + file_name, "wb"))

def normalize_similarity(similarity_vector):
    return (similarity_vector + 1.0)/2

def rename():
    root_dir = '../Aggregate'
    folder = 'CircuitYearLevel'
    updateRootDir(root_dir)
    files = getFilesListFromDir(folder, False)
    for file_name in files:
        file_name = root_dir + "/" + folder + "/" +file_name
        os.rename(file_name, file_name.replace('.0',''))

def main():
    rename()

if __name__ == "__main__":
    main()

