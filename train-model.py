from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib


df = pd.read_parquet("data.parquet")

X = df[["amount","location","device"]]
y = df["is_suspect"]

    
df_encoded = pd.get_dummies(X, columns=['location'])
X = pd.get_dummies(df_encoded, columns=['device'])

encoder = LabelEncoder()
y = encoder.fit_transform(y) 

# print(X)
# print(y)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

classifier = RandomForestClassifier(n_estimators = 100, max_depth=5, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
#print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(accuracy_score(y_test, y_pred))

joblib.dump(classifier, "model.pkl")