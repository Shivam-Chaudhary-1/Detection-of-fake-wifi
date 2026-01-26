import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
import joblib

df = pd.read_csv('wifi_dataset.csv')
X = df[['signal','channel','security','vendor','ssid']].copy()
y = df['is_fake']

X['ssid_len'] = X['ssid'].apply(lambda s: len(s))
X['ssid_has_special'] = X['ssid'].apply(lambda s: int(any(c in s for c in ['_','-','@'])))
X = X.drop(columns=['ssid'])

cat_cols = ['security','vendor']
pre = ColumnTransformer([('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)], remainder='passthrough')

clf = make_pipeline(pre, GradientBoostingClassifier(n_estimators=150, learning_rate=0.08))
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
clf.fit(X_train, y_train)
print('test score', clf.score(X_test,y_test))
joblib.dump(clf, 'model.pkl')
print('model saved: model.pkl')
