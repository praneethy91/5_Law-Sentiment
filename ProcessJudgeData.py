import pandas as pd
import os
import utils as utl

demo_local = True
local_path = "sentiment"
username = 'nk2239'
outDir = '/home/' + username + '/Aggregate/CaseLevel/'

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


def get_relative_path_of_cases():
    root_dir = 'data/clean_Mar_20'
    if demo_local:
        outDir = 'Aggregate/CaseLevel/'
    years=utl.getDirectoryList(outDir)
    if demo_local:
        years = ['1964']
    paths={}
    for year in years:
        if not year.endswith('zip') and year >= '1964':
            cases_files=utl.getFilesListFromDir(year)
            for case in cases_files:
                key = case.replace('-maj.p','')
                paths[key]=outDir + year+'/'+ case
    return paths


