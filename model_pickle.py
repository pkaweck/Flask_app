#Biblioteki

from pandas import read_csv
import pickle
from scikit-learn.model_selection import train_test_split
from scikit-learn.ensemble import RandomForestClassifier
from scikit-learn import metrics

df = read_csv('three_class_dataframe_performance.csv')

#train, test split
X = df.loc[:, df.columns!='class']
y = df.loc[:, df.columns == 'class']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)

#Create a Gaussian Classifier
clf=RandomForestClassifier(n_estimators=1000)

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X_train,y_train)
#Import scikit-learn metrics module for accuracy calculation

#predykcja nowych wartości
y_pred=clf.predict(X_test)
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",round(metrics.accuracy_score(y_test, y_pred), 2))

pickle.dump(clf, open('model.pkl', 'wb'))