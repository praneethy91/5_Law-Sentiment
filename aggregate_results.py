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
                for similarity in similarity_list:
                    similarity[:] = [util.normalize_similarity(score) for score in similarity]
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

def judge_level_accurate():
    data_frame = pjd.get_case_level_data_frame()
    judge_to_case_dict = pjd.create_dict_of_judges_cases(data_frame)
    case_to_path_dict = pjd.get_relative_path_of_cases()
    if demo_local :
        outDir = '../Aggregate'
    outDirectory = outDir + "/JudgeLevelAccurate"
    util.createDirectory(outDirectory)
    for judge, case_list in judge_to_case_dict.items():
        current_judge_score = np.zeros(40)
        case_count = 0
        for case_id in case_list:
            if case_id in case_to_path_dict:
                case_count += 1
                path=case_to_path_dict[case_id]
                current_score=pkl.load(open(path,'rb'))
                current_judge_score += current_score
        if case_count == 0:
            score = np.zeros(40)
        else:
            score = current_judge_score/case_count
        file = judge + '.p'
        util.writeToPickle(score, outDirectory, '', file)

def judge_level_usable():
    data_frame = pjd.get_case_level_data_frame()
    judge_to_case_dict = pjd.create_dict_of_judges_cases(data_frame)
    case_to_path_dict = pjd.get_relative_path_of_cases()
    if demo_local :
        outDir = '../Aggregate'
    outDirectory = outDir + "/JudgeLevelUsable"
    util.createDirectory(outDirectory)
    for judge, case_list in judge_to_case_dict.items():
        current_judge_score = np.zeros(40)
        case_count = 0
        for case_id in case_list:
            if case_id in case_to_path_dict:
                case_count += 1
                path=case_to_path_dict[case_id]
                current_score=pkl.load(open(path,'rb'))
                current_judge_score += current_score
        if not case_count == 0:
            score = current_judge_score/case_count
            file = judge + '.p'
            util.writeToPickle(score, outDirectory, '', file)

def circuityear_level():
    data_frame = pjd.get_case_level_data_frame()
    circuityear_case_dict = util.getDataFromPickle('circuit_year_level','../')
    case_to_path_dict = pjd.get_relative_path_of_cases()
    if demo_local :
        outDir = '../Aggregate'
    outDirectory = outDir + "/CircuitYearLevel"
    util.createDirectory(outDirectory)
    for circuityear, case_list in circuityear_case_dict.items():
        circuit=circuityear[0]
        year=circuityear[1]
        if year>1963:
            current_circuityear_score = np.zeros(40)
            case_count = 0
            for case_id in case_list:
                if case_id in case_to_path_dict:
                    case_count += 1
                    path=case_to_path_dict[case_id]
                    current_score=pkl.load(open(path,'rb'))
                    current_circuityear_score += current_score
            if not case_count == 0:
                score = current_circuityear_score/case_count
                file = '{0}_{1}.p'.format(circuit,year)
                util.writeToPickle(score, outDirectory, '', file)
            '''
            if case_count == 0:
                score = np.zeros(40)
            else:
                score = current_circuityear_score/case_count
            file = '{1}_{2}.p'.format(circuit,year)
            util.writeToPickle(score, outDirectory, '', file)
            '''

def check_case_exist():
    data_frame = pjd.get_case_level_data_frame()
    judge_to_case_dict = pjd.create_dict_of_judges_cases(data_frame)
    case_to_path_dict = pjd.get_relative_path_of_cases()
    if demo_local :
        outDir = '../Aggregate'
    outDirectory = outDir + "/JudgeLevelErrors"
    util.createDirectory(outDirectory)
    for judge, case_list in judge_to_case_dict.items():
        case_count = 0
        for case_id in case_list:
            if case_id in case_to_path_dict:
                case_count += 1
        if not case_count == len(case_list):
            file = judge + ".p"
            util.writeToPickle([len(case_list), case_count], outDirectory, '', file)


def main():
    pjd.update_demo_local(demo_local)
    #case_level()
    #judge_level()
    #check_case_exist()
    #judge_level_accurate()
    #judge_level_usable()
    circuityear_level()
if __name__ == "__main__":
    main()
