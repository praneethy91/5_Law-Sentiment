import pickle as pkl
import sklearn.linear_model as linear_model
from sklearn.model_selection import train_test_split
import numpy as np


demo_local = True
home_dir="/home/bsg348/"

if demo_local:
    home_dir = "../Regression_Data"

S_matrix_filename="S_matrix.pkl"
X_matrix_filename="X_matrix.pkl"
Z_matrix_filename="Z_matrix.pkl"

S_matrix=pkl.load(open(home_dir+S_matrix_filename,"rb"))
Z_matrix=pkl.load(open(home_dir+Z_matrix_filename,"rb"))
X_matrix=pkl.load(open(home_dir+X_matrix_filename,"rb"))

input_matrix=np.column_stack((Z_matrix,X_matrix))

X_train, X_test, y_train, y_test = train_test_split(input_matrix, S_matrix, test_size=0.1)
model = linear_model.LinearRegression()
model.fit(X_train, y_train)

y_predict=model.predict(X_test)

for i in range(len(y_predict)):
    print(y_test[i],y_predict[i],y_predict[i]-y_test[i])

diff=y_predict-y_test
mse=np.mean(diff**2)
print(np.sqrt(mse))