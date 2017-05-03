import pickle as pkl
import os
import sklearn.linear_model as linear_model
from sklearn.model_selection import train_test_split
import numpy as np

home_dir="/home/bsg348/"

#loading the matrices
#S_matrix is the similarity matrix
S_matrix_filename="S_matrix.pkl"
#X_matrix is the average unweighted judge biocharacteristics input matrix
X_matrix_filename="X_matrix.pkl"
#Z_matrix is the average weighted judge biocharacteristics input matrix
Z_matrix_filename="Z_matrix.pkl"
#gamma_ck is the fixed effect dummy matrix on circuit-target
gamma_ck_filename="gamma_ck"

#gamma_kt is the fixed effect dummy matrix on target year
gamma_kt_filename="gamma_ck"
S_matrix=pkl.load(open(home_dir+S_matrix_filename,"rb"))
Z_matrix=pkl.load(open(home_dir+Z_matrix_filename,"rb"))
X_matrix=pkl.load(open(home_dir+X_matrix_filename,"rb"))
gamma_ck=pkl.load(open(home_dir+gamma_ck_filename,"rb"))
gamma_kt=pkl.load(open(home_dir+gamma_kt_filename,"rb"))
#stacking them to form one single input matrix
input_matrix=np.column_stack((gamma_ck,gamma_kt,Z_matrix,X_matrix))

X_train_data, X_test_data, y_train_data, y_test_data = train_test_split(input_matrix, S_matrix, test_size=0.1)
model = linear_model.LinearRegression()
model.fit(X_train_data, y_train_data)
y_predict=model.predict(X_test_data)
diff=y_predict-y_test_data
mse=np.mean(diff**2)
print(np.sqrt(mse))

