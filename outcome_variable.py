import pandas as pd
import numpy as np
anes_data_inp=pd.read_stata("ANES_raw2008-1948.dta",convert_categoricals=False)
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
ranges=np.r_[1,112:151,645,646]
anes_data=anes_data_inp.iloc[:,ranges]
anes_data=anes_data[anes_data['VCF0004']>1963]
anes_data=anes_data[anes_data['VCF0901B']!='99']
anes_data['VCF0901A']=anes_data['VCF0901A'].map(circuit_mapping)
circuit_year_avg=anes_data.groupby(['VCF0004','VCF0901A']).mean()
circuit_year_avg.to_csv('outcome_variables.csv')