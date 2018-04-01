import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sbn
import numpy as np
import dateutil
from dateutil import parser
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn import svm,metrics,model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report
ChurnData=pd.read_csv("latest.csv")

#coverting string to datetime
ChurnData["InvoiceDate"]=pd.to_datetime(ChurnData["InvoiceDate"])

#initializing new features

#remove time and making index to Invoice Data
ChurnData["InvoiceDate"]=ChurnData["InvoiceDate"].apply(lambda ChurnData : datetime.datetime(day=ChurnData.day,month=ChurnData.month,year=ChurnData.year))

#plotting
times=ChurnData.Country.unique()
#g=sbn.FacetGrid(ChurnData,col="Monthly Regular")
#g.map(sbn.barplot,"Country",order=times)
#sbn.barplot(x="Monthly Regular",y="CustomerID",hue="Country",data=ChurnData)
#p1=sbn.kdeplot(ChurnData[ChurnData["Monthly Regular"]==1]["No of Diff Dates"],shade=True,color='b')
#p1=sbn.kdeplot(ChurnData[ChurnData["Monthly Regular"]==0]["No of Diff Dates"],shade=True,color='r')
#plt.show()

#making X and Y columns
take_columns=['CustomerID','Days bw Events','No of Diff Dates','MonthlyAmt','MonthlyEvents','DiffMonths']
X=ChurnData[take_columns]
Y=ChurnData["Monthly Regular"]
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=0)

scoring='accuracy'

#prepare model
models=[]
models.append(("LR",LogisticRegression()))
models.append(("LDA",LinearDiscriminantAnalysis()))
models.append((("KNN",KNeighborsClassifier())))
models.append(("CART",DecisionTreeClassifier()))
models.append(("NB",GaussianNB()))


#Cross Validation evaluate each model
print("Cross validation set for different classifiers are:")
results=[]
names=[]
for name,model in models:
    kfold=model_selection.KFold(n_splits=10,random_state=7)
    cv_results=model_selection.cross_val_score(model,X_train,Y_train,cv=kfold,scoring=scoring)
    results.append(cv_results)
    names.append(cv_results)
    names.append(name)
    msg="%s: %f (%f)" % (name,cv_results.mean(),cv_results.std())
    print(msg)

#applying logistic regression
logreg=LogisticRegression()
logreg.fit(X_train,Y_train)
Y_pred=logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, Y_test)))
#print(classification_report(Y_test,Y_pred))

#applying lda
ldaReg=LinearDiscriminantAnalysis()
ldaReg.fit(X_train,Y_train)
print('Accuracy of lda on test set: {:.2f}'.format(ldaReg.score(X_test, Y_test)))

#appling KNN
KnnReg=KNeighborsClassifier()
KnnReg.fit(X_train,Y_train)
print('Accuracy of Knn Classifier on test set: {:.2f}'.format(KnnReg.score(X_test, Y_test)))

#applying decision tree
dtReg=DecisionTreeClassifier()
dtReg.fit(X_train,Y_train)
print('Accuracy of Decision Tree on test set: {:.2f}'.format(dtReg.score(X_test, Y_test)))



