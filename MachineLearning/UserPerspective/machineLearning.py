# from sklearn.model_selection import cross_val_score, cross_val_predict, RandomizedSearchCV
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, VotingClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict, RandomizedSearchCV
import pandas as pd
from sklearn.svm import SVR
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# READ ALL DATA = TRAIN AND TEST TOGETHER
df = pd.read_csv('./spring_hourly_.csv')

# HACK: renaming columns to prevent format/conversion issues
df.columns = ['delta', 'latitude', 'longitude', 'station id', 'nhood', 'day', 'hour']
# print(df_data)

# Get lable
y = df['delta'].values

# Drop some columns and also the label
df.drop(['delta', 'nhood', 'station id'], axis=1, inplace=True)
# print(df_data)

# Create a new isWeekend column
bool_isWeekend = df['day'] > 4
isWeekend = 1 * bool_isWeekend
# print(isWeekend)
df['isWeekend'] = isWeekend
# print(df_data)

X = df.values # this does not have y labels

# Split data test/train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
# print("Training: ", len(X_test), " ", len(y_test), " ", len(X_train), " ", len(y_train))

# Regresion model: FIT + PREDICT
# y_lr = LinearRegression().fit(X_train, y_train).predict(X_test)
# y_rf = RandomForestRegressor().fit(X_train, y_train).predict(X_test)
# y_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1).fit(X_train, y_train).predict(X_test)
# y_lin = SVR(kernel='linear', C=1e3).fit(X_train, y_train).predict(X_test)
y_poly = SVR(kernel='poly', C=1e3, degree=2).fit(X_train, y_train).predict(X_test)

fig, ax = plt.subplots()
ax.scatter(y_test, y_poly, edgecolors=(0, 0, 0))
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()


# Cross validation
y_predict = cross_val_predict(rf, X, y, cv=3)
# score = cross_val_score(rf, X, y, cv=3)
# print(score)
mae = mean_absolute_error(y, y_predict)
mse = mean_squared_error(y, y_predict)
print("mae: ", mae)
print("mse: ", mse)

