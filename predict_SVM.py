from process_data import process_data

import sklearn
from sklearn import svm
from sklearn import metrics

from sklearn import preprocessing
max_abs_scaler = preprocessing.MaxAbsScaler()


def predict_svm(df_data):
    process = process_data(df_data)

    X, Y = process.data_classifier(y_key="open", classifier=True, prediction_day=7)
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.33)

    x_train = max_abs_scaler.fit_transform(x_train)
    x_test  = max_abs_scaler.fit_transform(x_test)

    model = svm.SVC(kernel='linear', gamma=2)
    model.fit(x_train, y_train.ravel())

    y_pred = model.predict(x_test)

    acc = metrics.accuracy_score(y_test, y_pred)
    return (acc)
