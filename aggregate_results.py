import ProcessJudgeData as pjd
import utils as util
import numpy as np
import pickle as pkl

username = 'nk2239'
outDir = '/home/' + username + '/Aggregate/'
demo_local = False

def case_level():
    sentiment_dir = '/home/' + username + '/VADER_DATA_STORE/'
    similarity_dir = '/home/' + username + '/SIMILARITY_DATA_STORE/'
    if(demo_local):
        sentiment_dir = 'VADER_DATA_STORE/'
        similarity_dir = 'SIMILARITY_DATA_STORE/'
        outDir = 'Aggregate'
    list_similarity_dir = util.getDirectoryList(similarity_dir)
    outDirectory = outDir + '/CaseLevel'
    for directory in list_similarity_dir:
        if not directory.endswith('zip'):
            util.createDirectory(outDirectory)
            util.createDirectory(outDirectory + "/" + directory)
            files = util.getFilesListFromDir(directory)
            for file in files:
                sentiment_list = util.getDataFromPickle(file, sentiment_dir + directory + '/')
                similarity_list = util.getDataFromPickle(file, similarity_dir + directory + '/')
                if(len(similarity_list) == len(sentiment_list)):
                    util.writeToPickle(np.dot(sentiment_list,similarity_list),outDir,directory,file)

def judge_level():
    data_frame = pjd.get_case_level_data_frame()
    judge_to_case_dict = pjd.create_dict_of_judges_cases(data_frame)
    case_to_path_dict = pjd.get_relative_path_of_cases()
    judges_to_score={}
    for judge, case_list in judge_to_case_dict.items():
        current_judge_score=None
        for case_id in case_list:
            path=case_to_path_dict[case_id]
            current_score=pkl.load(open(path,'rb'))
            if current_judge_score==None:
                current_judge_score=current_score
            else :
                current_judge_score+=current_score
        judges_to_score[judge]=current_judge_score/len(case_list)
    return judges_to_score

def main():
    case_level()
    #judge_level()



if __name__ == "__main__":
    main()
