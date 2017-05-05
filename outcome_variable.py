import pandas as pd
import numpy as np
import pickle as pk
import math
import os

anes_data_inp=pd.read_stata("data/ANES_raw2008-1948.dta",convert_categoricals=False)
circuit_mapping={
	23:1, 25:1, 33:1, 44:1,
	9:2, 36:2, 50:2,
	10:3, 34:3, 42:3,
	24:4, 37:4, 45:4, 51:4, 54:4,
	22:5, 28:5, 48:5,
	21:6, 26:6, 39:6, 47:6,
	17:7, 18:7, 55:7,
	5:8, 19:8, 27:8, 29:8, 31:8, 38:8, 46:8,
	2:9, 4:9, 6:9, 15:9, 16:9, 30:9, 32:9, 41:9, 53:9,
	8:10, 20:10, 35:10, 40:10, 49:10, 56:10,
	1:11, 12:11, 13:11,
	11:12
}

# Below is the sorted values of the state ID's in the ANES
# unique = anes_data_inp['VCF0901A'].unique()
# print(sorted([int(x) for x in unique if not math.isnan(x)]))

# Print the iloc of the columns of the last 4 instruments
# print(anes_data_inp.columns.get_loc("VCF9003"))
# print(anes_data_inp.columns.get_loc("VCF9004"))
# print(anes_data_inp.columns.get_loc("VCF9005"))
# print(anes_data_inp.columns.get_loc("VCF9006"))

ranges=np.r_[1,112:143,144:149,645,646, 813:817]
anes_data=anes_data_inp.iloc[:,ranges]
anes_data=anes_data[anes_data['VCF0004']>1963]
anes_data=anes_data[anes_data['VCF0901B']!='99']
anes_data['VCF0901A']=anes_data['VCF0901A'].map(circuit_mapping)
anes_data.ix[(anes_data["VCF0004"]<1981) &  (anes_data["VCF0901A"]==11),"VCF0901A"]=5
circuit_year_avg=anes_data.groupby(['VCF0004','VCF0901A']).mean()

sum = 0
for index, row in circuit_year_avg.iterrows():
	circuit = index[1]
	year = index[0]
	os.makedirs(os.path.join('data', 'outcome_var', str(circuit) + "_" + str(year)), exist_ok=True)
	pk.dump(row.values,
			open(os.path.join('data', 'outcome_var', str(circuit) + "_" + str(year), 'outcome_score'), 'wb'))

# Below is the sorted values of the state ID's which we are mapping to
# print(sorted([23, 25, 33, 44,
# 	9, 36, 50,
# 	10, 34, 42,
# 	24, 37, 45, 51, 54,
# 	22, 28, 48,
# 	21, 26, 39, 47,
# 	17, 18, 55,
# 	5, 19, 27, 29, 31, 38, 46,
# 	2, 4, 6, 15, 16, 30, 32, 41, 53,
# 	8, 20, 35, 40, 49, 56,
# 	1, 12, 13,
# 	11]))