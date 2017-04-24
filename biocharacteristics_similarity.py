import os
import pandas as pd

data_dir = 'data'
case_level_dta_file_name = 'BloombergCASELEVEL_Touse.dta'
case_level_dta_abs_path = os.path.abspath(os.path.join(data_dir, case_level_dta_file_name))
case_data_df = pd.read_stata(case_level_dta_abs_path)

judgeBioCharacteristics = ['party', 'Senior', 'gender', 'score']
judgePrefixes = ['j1', 'j2', 'j3']
allJudgesColumns = [(judgePrefix + characteristic)
                    for judgePrefix in judgePrefixes
                        for characteristic in judgeBioCharacteristics]

# Code for exploring the columns of the judge bio-characteristic data
# for column in allJudgesColumns:
#     print('------------------{0}-------------------'.format(column))
#     print(case_data_df[column].unique())

