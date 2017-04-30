import pandas as pd
import os
import utils as utl
import numpy as np

demo = True
check_same_val_for_multiple_key = True
demo_local = True
local_path = "sentiment"
username = 'nk2239'
outDir = '/home/' + username + '/Aggregate/CaseLevel/'


def update_demo_local(val):
    global demo_local
    demo_local = val

def get_case_level_data_frame():
    data_dir = 'data'
    if demo_local:
        data_dir = 'Bloomberg'
    case_level_dta_file_name = 'BloombergCASELEVEL_Touse.dta'
    case_level_dta_abs_path = os.path.abspath(data_dir + '/' + case_level_dta_file_name)
    case_data_df = pd.read_stata(case_level_dta_abs_path)
    sliced_data=case_data_df[['caseid','Author']]
    return sliced_data[sliced_data['Author']!='']


def create_dict_of_judges_cases(data_frame):
    judges_dict={}
    cases_data = data_frame
    for index,row in cases_data.iterrows():
      if not row['Author'] in judges_dict:
        judges_dict[row['Author']]=[]
      judges_dict[row['Author']].append(row['caseid'])
    return judges_dict


def find_diff_files(same_dict):
    for key in same_dict:
        if len(same_dict[key]) > 1:
            comp_orig = utl.getDataFromPickle('',same_dict[key][0])
            for val in same_dict[key]:
                comp_new = utl.getDataFromPickle('',val)
                if not np.array_equal(comp_new,  comp_orig):
                    print(key)
                    print(comp_orig)
                    print(comp_new)


def create_repeat_set(same_dict):
    case_set = set()
    for key in same_dict:
        case_set.add(key)
    return case_set


def get_relative_path_of_cases():
    root_dir = 'data/clean_Mar_20'
    if demo_local:
        outDir = '../Aggregate/CaseLevel/'
    years=utl.getDirectoryList(outDir)
    #if demo_local:
    #   years = ['1964']
    paths={}
    same_dict = {}
    for year in years:
        if not year.endswith('zip') and year >= '1964':
            cases_files=utl.getFilesListFromDir(year, False)
            for case in cases_files:
                key = case.replace('-maj.p','')
                key += str(year)
                paths[key] = outDir + year + '/' + case
                if check_same_val_for_multiple_key:
                    if not key in same_dict:
                        same_dict[key] = []
                    same_dict[key].append(outDir + year+'/'+ case)
    if check_same_val_for_multiple_key:
        case_set = create_repeat_set(same_dict)
        #find_diff_files(same_dict)
    return paths, case_set

def main():
    if demo == True:
        case_to_path_dict = get_relative_path_of_cases()
        print(case_to_path_dict)

if __name__ == "__main__":
    main()