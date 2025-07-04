import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from keras.constraints import maxnorm
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, KFold, RandomizedSearchCV

#a
gas_turbines = pd.read_csv("gas_turbines.csv")
gas_turbines.head()

#b
gas_turbines.info()

#c
sns.set_style('darkgrid')
sns.pairplot(gas_turbines)
plt.show()

#d
"""color = ["g","y","r", "b","g","y","r", "b","g","y","r"]
for i,j in zip(gas_turbines.columns.values,color):
f, axes = plt.subplots(figsize=(10,8))
sns.regplot(x = 'TEY', y = i, data = gas_turbines,color = j, scatter_kws={'alpha':0.3})
axes.set_xlabel('TEY', fontsize = 14)
axes.set_ylabel(i, fontsize=14)
plt.show()"""

#e
import seaborn as sns
import matplotlib.pyplot as pplt
#correlation matrix
corrmat = gas_turbines.corr()
f, ax = plt.subplots(figsize=(20, 15))
sns.heatmap(corrmat, vmax=.8, square=True, annot=True);
y = gas_turbines[gas_turbines.columns[7]]
X = gas_turbines[['AT', 'AP', 'AH', 'AFDP', 'GTEP', 'TIT', 'TAT', 'CDP', 'CO','NOX']]

#f
# correlation with TEY
data2 = X.copy()
correlations = data2.corrwith(gas_turbines["TEY"])
correlations = correlations[correlations!=1]
positive_correlations = correlations[correlations >0].sort_values(ascending = False)
negative_correlations =correlations[correlations<0].sort_values(ascending = False)
correlations.plot.bar(
figsize = (20, 10),
fontsize = 16,
color = 'r',
rot = 80, grid = True)
plt.title('Correlation with Turbine energy yield \n',
horizontalalignment="center", fontstyle = "normal",
fontsize = "20", fontfamily = "sans-serif")
# split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
#feature selecton
def select_features(X_train, y_train, X_test):
# configure to select all features
features = SelectKBest(score_func=mutual_info_regression, k='all')
# Relationships from training data
features.fit(X_train, y_train)
# transform train data
X_train_f = features.transform(X_train)
# transform test data
X_test_f = features.transform(X_test)
return X_train_f, X_test_f, features

#g
X_train_f, X_test_f, features = select_features(X_train, y_train, X_test)
fig, axes = plt.subplots(figsize=(10, 8))
plt.bar([i for i in range(len(features.scores_))], features.scores_)
axes.set_xticks([0,1,2,3,4,5,6,7,8,9])
axes.set_xticklabels(X.columns.values)
plt.show()

#h
y_copy = gas_turbines["TEY"]
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
y_ = StandardScaler().fit_transform(y_copy.values.reshape(len(y_copy),1))[:,0]
X1 = gas_turbines.drop(['TEY','AT','AP','AH','CO','NOX'], axis = 1)
scaler.fit(X1)
#X_copy = X[['AFDP', 'GTEP', 'TIT', 'TAT', 'CDP']]
features_scaler=scaler.fit_transform(X1)
X_=pd.DataFrame(features_scaler,columns=X[['AFDP', 'GTEP', 'TIT', 'TAT', 'CDP']].columns)
X_.head()
# Splitting data into test data and train data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X1, y_, test_size=0.3, random_state=1)

#i
print('Shape of x_train: ', X_train.shape)
print('Shape of x_test: ', X_test.shape)
print('Shape of y_train: ', y_train.shape)
print('Shape of y_test: ', y_test.shape)
model = Sequential()
model.add(Dense(28, input_dim=5, kernel_initializer='uniform', activation='tanh'))
model.add(Dense(50, kernel_initializer='uniform', activation='tanh'))
model.add(Dense(50, kernel_initializer='uniform', activation='tanh'))
model.add(Dense(1, kernel_initializer='uniform', activation='linear'))
# Compile model
model.compile(loss='mean_squared_error', optimizer='adam',
metrics=['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error',
'cosine_proximity'])

#j
model.summary()

#k
# Fit the model
history = model.fit(X_train,y_train, epochs=500)
# model evaluation
scores = model.evaluate(X_test, y_test)
print((model.metrics_names[1]))

#l
fig, axes = plt.subplots(figsize=(20, 8))
# plot metrics
plt.plot(history.history['mean_squared_error'])
"""plt.plot(history.history['mean_absolute_error'])
plt.plot(history.history['mean_absolute_percentage_error'])
plt.plot(history.history['cosine_proximity'])
"""
plt.show()

#m
y2 = gas_turbines["TEY"]
data_c = gas_turbines.copy()
X2 = data_c.drop(['TEY','AT','AP','AH','CO','NOX'], axis = 1)
# Scaling all the features
scaler.fit(X2)
y2_ = StandardScaler().fit_transform(y2.values.reshape(len(y2),1))[:,0]
scaled_features=scaler.transform(X2)
data_head=pd.DataFrame(scaled_features,columns=X2.columns)
data_head.head()
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
x_train, x_test, y_train, y_test = train_test_split(X2, gas_turbines["TEY"], test_size=0.3, random_state=42)

#n
def create_model(learning_rate,dropout_rate,activation_function,init,neuron1,neuron2):
model = Sequential()
model.add(Dense(neuron1,input_dim = 5,kernel_initializer = init,activation = activation_function))
model.add(Dropout(dropout_rate))
model.add(Dense(neuron2,input_dim = neuron1,kernel_initializer = init,activation = activation_function))
model.add(Dropout(dropout_rate))
model.add(Dense(1,activation = 'linear'))
adam=Adam(learning_rate = learning_rate)
model.compile(loss = 'mean_squared_error',optimizer = adam, metrics = ['mse'])
return model
# Create the model
model = KerasClassifier(build_fn = create_model,verbose = 0)
# Define the grid search parameters
batch_size = [20,40]
epochs = [100,500]
learning_rate = [0.01,0.1]
dropout_rate = [0.1,0.2]
activation_function = ['softmax','relu','tanh','linear']
init = ['uniform','normal']
neuron1 = [4,8,16]
neuron2 = [2,4,8]
# Make a dictionary of the grid search parameters
param_grids = dict(batch_size = batch_size,epochs = epochs,learning_rate = learning_rate,dropout_rate =
dropout_rate,
activation_function = activation_function,init = init,neuron1 = neuron1,neuron2 = neuron2)
# Build and fit the GridSearchCV
grid = GridSearchCV(estimator = model,param_grid = param_grids,cv = KFold(),verbose = 10,
scoring='neg_mean_squared_error')
grid_result = grid.fit(x_train, y_train)
# Summarize the results
print('Best : {}, using {}'.format(grid_result.best_score_,grid_result.best_params_))
# Summarize the results
print('Best : {}, using {}'.format(grid_result_cv.best_score_,grid_result.best_params_))
means = grid_result_cv.cv_results_['mean_test_score']
stds = grid_result_cv.cv_results_['std_test_score']
params = grid_result_cv.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
print('{},{} with: {}'.format(mean, stdev, param))
