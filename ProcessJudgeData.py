import pandas as pd
import os

data_dir = 'data'
case_level_dta_file_name = 'BloombergCASELEVEL_Touse.dta'
case_level_dta_abs_path = os.path.abspath(data_dir + '/' + case_level_dta_file_name)

case_data_df = pd.read_stata(case_level_dta_abs_path)

# Print the authors of the DataFrame
# print(case_data_df['Author'].head(100))