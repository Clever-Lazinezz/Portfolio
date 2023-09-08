

import get_data_and_statistics as gds
import normalizing_data as nd


from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report ,confusion_matrix
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics # auc
from sklearn.metrics import f1_score


# Gradient Boosted Trees (GBM)
"""

individual_complete_project = gds.gather_joined_projects()
gds.make_data_uniform(individual_complete_project)
df = individual_complete_project[1]
nd.catolino2019_normalization(df)
X = df.drop(columns=['bug'], axis = 1)
y = df['bug']

X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.30, random_state  = 101)
rfc = RandomForestClassifier(n_estimators = 600)
rfc.fit(X_train,y_train)

predictions = rfc.predict(X_test)
print(classification_report(y_test,predictions))

"""


individual_complete_project = gds.gather_joined_projects()
gds.make_data_uniform(individual_complete_project)
df = individual_complete_project[0]

# df_cat = individual_complete_project[1]
nd.fan2019_normilization(df)
# nd.catolino2019_normalization(df)
# nd.kamei2012_normalization(df)
# nd.mcintosh2017_normilization(df)


# Not inplace, only a copy dataframe
X = df.drop(columns=['bug'], axis = 1)
y = df['bug']
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.30, random_state  = 101)

# print(df['fix'].value_counts())

rfc = RandomForestClassifier(n_estimators = 600)
rfc.fit(X_train,y_train)

predictions = rfc.predict(X_test)
print(classification_report(y_test,predictions))



"""
A = df_cat.drop(columns=['fix', 'bug'], axis = 1)
b = df_cat['fix']
A_train,A_test,b_train,b_test = train_test_split(A, b, test_size = 0.30, random_state  = 101)


print(X.columns, "\n\n", A.columns, "\n\n\n")


predictions = rfc.predict(X_test)
print(classification_report(y_test,predictions))

print("\n\n\n")

predictions = rfc.predict(A_test)
print(classification_report(b_test,predictions))
"""



"""

##########################################################


X = df.drop(columns=['fix'], axis = 1)
y = df['fix']
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.30, random_state  = 101)


dtree = DecisionTreeClassifier()
dtree.fit(X_train, y_train)
predictions = dtree.predict(X_test)


print(classification_report(y_test, predictions))
print(confusion_matrix(y_test, predictions))


##########################################################


# better than decision tree
X = df.drop(columns=['fix'], axis = 1)
y = df['fix']
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.30, random_state = 101)
rfc = RandomForestClassifier(n_estimators = 600)
rfc.fit(X_train,y_train)
predictions = rfc.predict(X_test)
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))


##########################################################




X = df.drop(columns=['fix'], axis = 1)
y = df['fix']
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.30, random_state  = 101)

rfc = RandomForestClassifier(n_estimators = 600)
rfc.fit(X_train,y_train)

for X_test in individual_complete_project:
    X_test.drop(columns=['fix'], axis=1, inplace=True)
    predictions = rfc.predict(X_test)
    print(classification_report(y_test,predictions))




# %%
z = individual_complete_project[1]
# z.isnull().value_counts()
z.info()
medians = z.median()
z.fillna(value=medians, inplace=True)
z.info()
# %%

"""
