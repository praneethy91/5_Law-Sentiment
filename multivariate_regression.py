import pickle
import sklearn.linear_model as linear_model
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.feature_selection import SelectFromModel


demo_local = True
home_dir="/home/bsg348/"

if demo_local:
    home_dir = "../Regression_Data/"

S_matrix_filename="S_matrix.pkl"
X_matrix_filename="X_matrix.pkl"
Z_matrix_filename="Z_matrix.pkl"

S_matrix=pickle.load(open(home_dir+S_matrix_filename,"rb"))
Z_matrix=pickle.load(open(home_dir+Z_matrix_filename,"rb"))
X_matrix=pickle.load(open(home_dir+X_matrix_filename,"rb"))
input_matrix=np.column_stack((Z_matrix,X_matrix))


def checkResults(y_predict, y_test):
    for i in range(len(y_predict)):
        print(y_test[i], y_predict[i], y_predict[i] - y_test[i])

    diff = y_predict - y_test
    mse = np.mean(diff ** 2)
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
    X_train, X_test, y_train, y_test = train_test_split(input_matrix, S_matrix, test_size=0.1)
    model = regression(X_train, y_train)
    predict(model, X_test, y_test)


if __name__ == "__main__":
    main()

