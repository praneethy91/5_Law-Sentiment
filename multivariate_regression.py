import pickle
import pandas as pd
import sklearn.linear_model as linear_model
from sklearn.linear_model import ElasticNetCV
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
import numpy as np
import os
from sklearn.linear_model import LassoCV
from sklearn.feature_selection import SelectFromModel


demo_local = True
home_dir="/home/bsg348/"

if demo_local:
    home_dir = "data/"

S_matrix_filename="S_matrix.pkl"
Z_matrix_filename="Z_matrix.pkl"
Y_matrix_filename="Y_matrix.pkl"

#gamma_ck is the fixed effect dummy matrix on circuit-target
gamma_ck_filename="gamma_ck"

#gamma_kt is the fixed effect dummy matrix on target year
gamma_kt_filename="gamma_kt"

#gamma_ct is the fixed effect dummy matrix on circuit year
gamma_ct_filename="gamma_ct"

S_matrix=pickle.load(open(home_dir+S_matrix_filename,"rb"))
Z_matrix=pickle.load(open(home_dir+Z_matrix_filename,"rb"))
Y_matrix=pickle.load(open(home_dir+Y_matrix_filename,"rb"))
gamma_ck=pickle.load(open(home_dir+gamma_ck_filename,"rb"))
gamma_kt=pickle.load(open(home_dir+gamma_kt_filename,"rb"))
gamma_ct=pickle.load(open(home_dir+gamma_ct_filename,"rb"))

input_matrix=np.column_stack((gamma_ck, gamma_kt, gamma_ct, Z_matrix))

def checkResults(y_predict, y_test):
    #for i in range(len(y_predict)):
    #    print(y_test[i], y_predict[i], y_predict[i] - y_test[i])

    diff = y_predict - y_test
    mse = np.mean(np.square(diff))
    print(np.sqrt(mse))


'''
def feature_selection(df, target, model = LassoCV()):
    characteristics_cols = [col for col in list(df) if col.startswith('x_')]
    # characteristics_cols += [col for col in list(df) if col.startswith('e_x_')]
    # characteristics_cols += [col for col in list(df) if col.startswith('dummy_')]
    X, y = df[characteristics_cols].fillna(0), df[target]
    # clf = LassoCV()
    # Use ExtraTreesClassifier() for Random Forest
    sfm = SelectFromModel(model, threshold=0)
    sfm.fit(X, y)

    n_features = sfm.transform(X).shape[1]

    # Reset the threshold till the number of features equals two.
    # Note that the attribute can be set directly instead of repeatedly
    # fitting the metatransformer.
    while n_features > 5:
        sfm.threshold += 0.05
        X_transform = sfm.transform(X)
        n_features = X_transform.shape[1]

    features_selected = [x for (x, y) in zip(characteristics_cols, sfm.get_support()) if y == True]
    return features_selected
'''

def regression(X_train, y_train):
    #features = feature_selection(X_train, y_train)
    model = linear_model.LinearRegression(normalize=True)
    model.fit(X_train, y_train)
    return model


def predict(model, X_test, y_test):
    y_predict = model.predict(X_test)
    checkResults(y_predict, y_test)


def main():
    # X is the endogenous regressor (S_ckt)
    # Z are the instruments (biocharacteristics, weighted and unweighted in a circuit-year)
    Z = input_matrix
    X = S_matrix

    #Implementing a plain regression model
    #model = regression(X_train, y_train)
    #print("Using plain Linear regression. MSE below:")
    #predict(model, X_train, y_train)

    # de-mean and standardize (optional)
    X = (X - X.mean()) / X.std()
    Z = (Z - Z.mean()) / Z.std()

    # N is the number of datapoints
    # Q is the number of instruments
    # We have only one endogenous regressor
    N = X.shape[0]
    Q = Z.shape[1]

    enetcv = ElasticNetCV(l1_ratio=[.01, .1, .5, .7, .9, .99, 1], n_alphas=20, n_jobs=4,
                          selection='cyclic', max_iter=50000, tol=1e-4)

    #TODO: Do we need Fstats?

    # fit elastic net
    X = X.flatten()
    enetcv.fit(Z, X)
    Xhat_enet = enetcv.predict(Z)

    # save index of non-zero coefficients in enetZ
    enetZ = np.where(enetcv.coef_ != 0)[0]

    # Number of instruments selected
    numSelected = len(enetZ)

    print("Total number of data points: {0}".format(N))
    print("Total number of instruments: {0}".format(Q))
    print("Number of instruments selected: {0}".format(numSelected))

    # if all zeros, None of the instruments are correlated to X
    if numSelected == 0:
        print("None of the instruments are good. Skipping OLS.")
        return
    else:
        # run OLS with selected instruments
        postenet = sm.OLS(X, Z[:, enetZ]).fit()  # (cov_type='cluster',cov_kwds={'groups':(clusters)})
        print(postenet.summary())

        # Save the predicted endogenous regressor vector of X
        Xhat_post_enet = postenet.predict()

    os.makedirs(os.path.join('data', 'OLS'), exist_ok=True)
    pd.to_pickle(enetZ, os.path.join('data','OLS','enetZ.pkl'))
    pd.to_pickle(Xhat_enet, os.path.join('data','OLS','Xhat-enet.pkl'))
    pd.to_pickle(Xhat_post_enet, os.path.join('data','OLS','Xhat-post-enet.pkl'))

if __name__ == "__main__":
    main()

