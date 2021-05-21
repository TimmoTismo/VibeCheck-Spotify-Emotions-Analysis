from sklearn import svm
import pandas as pd
import math
from sklearn.model_selection import train_test_split

#Reading in the CSV file
data = pd.read_csv('datasets/data_by_genres.csv')
print(data.head(6))

all_X = data.iloc[:, 1:13] # All rows, features only, no labels
all_y = data.iloc[:, 13] # All rows, label only, no features


#Preprocess the data
X_train, X_test, y_train, y_test = train_test_split(all_X, all_y)


#Train and Evaluate the model
clf = svm.SVC()
#print(type(y_train))
clf.fit(X_train, y_train)

clf.score(X_test,  y_test)


#Predict on some new data
clf.predict(X_test[10:15])

y_test[10:15]