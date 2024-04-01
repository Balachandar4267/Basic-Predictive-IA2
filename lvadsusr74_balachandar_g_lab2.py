# -*- coding: utf-8 -*-
"""LVADSUSR74- BALACHANDAR G - Lab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LzT3pvf2YVkNNayQ4epCIfX6eRgLfxCm
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,mean_absolute_error
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("/content/sample_data/Mall_Customers.csv")
df.info()

df.isnull().sum()
df.fillna(method ='ffill',inplace = True)
df.fillna(method = 'bfill',inplace = True)

df.isnull().sum()

df.duplicated().sum()
df.drop_duplicates()

plt.figure(figsize=(10,6))
sns.boxplot(data = df)
plt.title("Identifying outliers")
plt.show()

#removing outliers
df_55=pd.DataFrame(df)

iso = IsolationForest(contamination=0.1)
outliers = iso.fit_predict(df_55['Annual Income (k$)'].values.reshape(-1,1))

#print(outliers)
dd=df.drop(df_55.iloc[np.where(outliers== -1)].index,inplace=False)
print("The removed outliers:","\n",dd)

plt.figure(figsize = (10,6))
sns.boxplot(data = dd)
plt.title("After Removing outliers")
plt.show()

df1=pd.get_dummies(dd,columns=["Gender"])

df1.drop('Gender_Female',axis=1,inplace=True)
df1.head()

df1['Annual Income (k$)'].plot(kind='hist', bins=20, title='Annual Income (k$)')
plt.gca().spines[['top', 'right',]].set_visible(False)

#visulation
df1['CustomerID'].plot(kind='line', figsize=(8, 4), title='CustomerID')
plt.gca().spines[['top', 'right']].set_visible(False)

scaler = MinMaxScaler()
scaler.fit(df1[['Annual Income (k$)']])
df1['Annual Income (k$)'] = scaler.transform(df1[['Annual Income (k$)']])
scaler.fit(df1[['Age']])
df1['Age'] = scaler.transform(df1[['Age']])
print(df1.head())
plt.scatter(df1.Age,df1['Annual Income (k$)'])

km = KMeans(n_clusters=3)
y_predicted = km.fit_predict(df1[["Annual Income (k$)","Age"]])
#y_predicted
df1['cluster']=y_predicted
df1.head(25)
print(km.cluster_centers_)

df11 = df1[df1.cluster==0]
df12 = df1[df1.cluster==1]
df13 = df1[df1.cluster==2]
#df14 = df1[df1.cluster==3]
#df5 = df[df.cluster==4]
plt.scatter(df11.Age,df11['Annual Income (k$)'],color='green')
plt.scatter(df12.Age,df12['Annual Income (k$)'],color='red')
plt.scatter(df13.Age,df13['Annual Income (k$)'],color='yellow')
#plt.scatter(df14.Age,df14['Annual Income (k$)'],color='orange')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')
plt.xlabel('Age')
plt.ylabel('Annual Income')
plt.legend()

sse = []
k_rng = range(1,10)
for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit(df1[['Age','Annual Income (k$)']])
    sse.append(km.inertia_)

plt.xlabel('K')
plt.ylabel('Sum of squared error')
plt.plot(k_rng,sse)