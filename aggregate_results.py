import ProcessJudgeData as pjd
import utils as util
import numpy as np

username = 'nk2239'
outDir = '/home/' + username + '/Aggregate/'

def case_level():
    sentiment_dir = '/home/' + username + '/VADER_DATA_STORE/'
    similarity_dir = '/home/' + username + '/SIMILARITY_DATA_STORE/'
    list_similarity_dir = util.getDirectoryList(similarity_dir)
    outDirectory = outDir + '/CaseLevel'
    for directory in list_similarity_dir:
        util.createDirectory(outDirectory)
        util.createDirectory(outDirectory + "/" + directory)
        files = util.getFilesListFromDir(directory)
        for file in files:
            sentiment_list = util.getDataFromPickle(file, sentiment_dir + directory + '/')
            similarity_list = util.getDataFromPickle(file, similarity_dir + directory + '/')
            if(len(similarity_list) == len(sentiment_list)):
                util.writeToPickle(np.dot(sentiment_list,similarity_list),outDir,directory,file)

def judge_level(judge_to_case_dict, case_to_path_dict):
    for judge, case_list in judge_to_case_dict.items():
        for case_id in case_list:
            path=case_to_path_dict[case_id]
            #To do Bhaskar
            #file_to_load=open(())
    return

def main():
    data_frame = pjd.get_case_level_data_frame()
    judge_to_case = pjd.create_dict_of_judges_cases(data_frame)
    case_to_path = pjd.get_relative_path_of_cases()
    case_level()
    judge_level(judge_to_case, case_to_path)



if __name__ == "__main__":
    main()
