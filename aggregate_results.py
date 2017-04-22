import ProcessJudgeData as pjd
import utils as util
import numpy as np
import pickle as pkl

username = 'nk2239'
outDir = '/home/' + username + '/Aggregate/'
demo_local = True

def case_level():
    sentiment_dir = '/home/' + username + '/VADER_DATA_STORE/'
    similarity_dir = '/home/' + username + '/SIMILARITY_DATA_STORE/'
    if(demo_local):
        sentiment_dir = '../VADER_DATA_STORE'
        similarity_dir = '../SIMILARITY_DATA_STORE'
        outDir = '../Aggregate'
    list_similarity_dir = util.getDirectoryList(similarity_dir)
    outDirectory = outDir + '/CaseLevel'
    for directory in list_similarity_dir:
        if not directory.endswith('zip'):
            util.createDirectory(outDirectory)
            util.createDirectory(outDirectory + "/" + directory)
            files = util.getFilesListFromDir(directory, False)
            for file in files:
                sentiment_list = util.getDataFromPickle(file, sentiment_dir + "/" + directory + '/')
                similarity_list = util.getDataFromPickle(file, similarity_dir + "/" + directory + '/')
                if len(similarity_list) == len(sentiment_list):
                    ss = np.dot(sentiment_list, similarity_list)
                    if len(sentiment_list) == 0:
                        util.writeToPickle(0, outDirectory, directory, file)
                    else:
                        util.writeToPickle(ss/len(sentiment_list),outDirectory,directory,file)

def judge_level():
    data_frame = pjd.get_case_level_data_frame()
    judge_to_case_dict = pjd.create_dict_of_judges_cases(data_frame)
    case_to_path_dict = pjd.get_relative_path_of_cases()
    if demo_local :
        outDir = '../Aggregate'
    outDirectory = outDir + "/JudgeLevel"
    util.createDirectory(outDirectory)
    for judge, case_list in judge_to_case_dict.items():
        current_judge_score = np.zeros(40)
        for case_id in case_list:
            if case_id in case_to_path_dict:
                path=case_to_path_dict[case_id]
                current_score=pkl.load(open(path,'rb'))
                current_judge_score += current_score
        if len(case_list) == 0:
            score = np.zeros(40)
        else:
            score = current_judge_score/len(case_list)
        file = judge + '.p'
        util.writeToPickle(score, outDirectory, '', file)

def main():
    pjd.update_demo_local(demo_local)
    case_level()
    judge_level()

if __name__ == "__main__":
    main()
