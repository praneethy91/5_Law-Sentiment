import pickle
import os
import numpy as np
import statsmodels.sandbox.regression.gmm

home_dir = ""

S_matrix_filename="S_matrix.pkl"
S_matrix_filename_new="S_matrix_new.pkl"
Z_matrix_filename="Z_matrix.pkl"
Y_matrix_filename="Y_matrix.pkl"

#gamma_ck is the fixed effect dummy matrix on circuit-target
gamma_ck_filename="gamma_ck"

#gamma_kt is the fixed effect dummy matrix on target year
gamma_kt_filename="gamma_kt"

#gamma_ct is the fixed effect dummy matrix on circuit year
gamma_ct_filename="gamma_ct_new"

gamma_ck=pickle.load(open(home_dir+gamma_ck_filename,"rb"))
gamma_kt=pickle.load(open(home_dir+gamma_kt_filename,"rb"))
gamma_ct=pickle.load(open(home_dir+gamma_ct_filename,"rb"))

selected_instruments_index = pickle.load(open(os.path.join('data','OLS','enetZ.pkl'),"rb"))

endogeneous_matrix=pickle.load(open(home_dir + S_matrix_filename, "rb"))
dependent_matrix=pickle.load(open(home_dir + Y_matrix_filename, "rb"))
Z_matrix=pickle.load(open(home_dir + Z_matrix_filename, "rb"))

S_matrix_new=pickle.load(open(home_dir + S_matrix_filename_new, "rb"))
S_matrix_new=S_matrix_new.reshape((S_matrix_new.shape[0],1))
instrument_matrix=np.column_stack((S_matrix_new, Z_matrix))
idx =   [x-238 for x in selected_instruments_index if x>239]
instrument_matrix = instrument_matrix[:, idx]

# dependent_matrix = (dependent_matrix - dependent_matrix.mean()) / dependent_matrix.std()
# endogeneous_matrix = (endogeneous_matrix - endogeneous_matrix.mean()) / endogeneous_matrix.std()
# instrument_matrix = (instrument_matrix - instrument_matrix.mean()) / instrument_matrix.std()

print(dependent_matrix.shape)
print(endogeneous_matrix.shape)
print(instrument_matrix.shape)

x = statsmodels.sandbox.regression.gmm.IV2SLS(dependent_matrix, endogeneous_matrix, instrument_matrix)

x.fit()
results = x._results_ols2nd
print(results.summary())