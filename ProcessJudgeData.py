import pandas as pd
import os
import utils as utl

def get_case_level_data_frame():
	data_dir = 'data'
	case_level_dta_file_name = 'BloombergCASELEVEL_Touse.dta'
	case_level_dta_abs_path = os.path.abspath(data_dir + '/' + case_level_dta_file_name)

	case_data_df = pd.read_stata(case_level_dta_abs_path)

	sliced_data=case_data_df[['caseid','Author']]
	return sliced_data[sliced_data['Author']!='']



def create_dict_of_judges_cases():
	judges_dict={}
	cases_data=get_case_level_data_frame()
	for index,row in cases_data.iterrows():
	  if not row['Author'] in judges_dict:
	    judges_dict[row['Author']]=[]
	  judges_dict[row['Author']].append(row['caseid'])

	return judges_dict 

def get_relative_path_of_cases():
	years=utl.getDirectoryList(utl.root_dir)
	paths={}
	for year in years:
		if not year.endswith('zip'):
			cases_files=utl.getFilesListFromDir(year)
			for case in cases_files:
				paths[case]=utl.root_dir + "/" + year + '/maj/' + case
	return paths


