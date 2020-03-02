import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, ExtraTreesClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, recall_score, precision_score, accuracy_score
from sklearn import metrics
from cleaning_pipeline import *
from EDA import *
import scipy.stats as scs
import statsmodels.api as sm
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from statsmodels.formula.api import ols
from statsmodels.compat import lzip
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
import seaborn as sns
from sklearn import (
    cluster, datasets, 
    decomposition, ensemble, manifold, 
    random_projection, preprocessing)

plt.rcParams.update({'font.size': 22})

def summary_model(X, y, label='scatter'):
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    summary = model.summary()
    return summary

def plot_feat_imp(idx, features, feat_importances,  n = 5, fname = 'images/test.jpeg'):
    '''
    Plot the top n features.
    '''
    labels = np.array(features)[idx[:n]]
    fig, ax = plt.subplots(1,1, figsize = (10,5))
    ax.barh(range(n), feat_importances[idx[:n]], color = 'b', alpha = 0.85)
    # ax.set_xticklabels(labels)
    ax.set_title('Feature Importance')
    plt.yticks(ticks = range(n), labels = labels)
    plt.tight_layout(pad = 1)
    plt.savefig(fname)
    plt.show()

if __name__ == '__main__':
    
    X_fm = pd.read_csv('../data/clean/feature_matrix_X_final_1.csv')
    y_fm = pd.read_csv('../data/clean/feature_matrix_y_final.csv')
    
  
    y_fm.fillna(0, inplace = True)

    X_fm.fillna(0, inplace = True)
    X_fm.drop('Unnamed: 0', inplace = True, axis = 1)
    X_fm.drop('well_count', inplace = True, axis = 1)
    y_fm.drop('Unnamed: 0', inplace = True, axis = 1)

    X_fm = X_fm.set_index('year')
    y_fm = y_fm.set_index('year')
    
    year = [2001, 1978, 1977]
  
    X_fm = X_fm.drop(year, axis = 0)
   
    X_train_mask = X_fm.index < 2014
    X_test_mask = X_fm.index >= 2014
    y_train_mask = y_fm.index < 2014
    y_test_mask = y_fm.index >= 2014

    X_train = X_fm[X_train_mask]
    X_test = X_fm[X_test_mask]
    y_train = y_fm[y_train_mask]
    y_test = y_fm[y_test_mask]

    x_18= X_test.loc[2018, : ]
    m= x_18.values > 115000000
    cols_keep = np.array(X_test.columns)[m]
    cols_keep = np.append(cols_keep, 'psi')
    X_train = X_train[cols_keep]
    X_test = X_test[cols_keep]
  

    full_data = X_fm.merge(y_fm, how='outer', left_index=True, right_index=True)

#Run Linear Regression
    summery = summary_model(X_train, y_train, label='scatter')
    reg = LinearRegression().fit(X_train,y_train)
    reg.score(X_train, y_train)
    y_pred = reg.predict(X_test)
    print('MSE = ', mean_squared_error(y_test,y_pred))
    
# Run Random Forest Regressor 

    rf = RandomForestRegressor(n_estimators=100, random_state=0,bootstrap = False)
    rf.fit(X_train, y_train.values.ravel())
    predictions = rf.predict(X_test)

    test_values = y_test.values
    errors = abs(predictions - test_values )
    
    # Calculate mean absolute percentage error (MAPE)
    mape = np.mean(100 * (errors / test_values))

    # Calculate accuracy
    accuracy = 100 - mape
   


    
    feat_importances = rf.feature_importances_
    idx = np.argsort(rf.feature_importances_)[::-1]
    features = ['Barlesville','Arbuckle','2nd Wilcox','Wilcox','Viola','Hunton','Pontotoc','Deese','Healdton','Douglas','Arbuckle Group','Hoxbar-Deese','Multiples','PSI']
    plot_feat_imp(idx, features, feat_importances,  n = 11, fname = '../images/rf_feature_importances.png')




    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test.values.ravel(), y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(y_test.values.ravel(), y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test.values.ravel(), y_pred)))

    print('Metrics for Random Forest Trained on Data with Formations')
    print('Average absolute error:', round(np.mean(errors), 2), 'Earthquakes')
    print('Accuracy:', round(accuracy, 2), '%.')



# Simple matrices 

    X_simple = pd.read_csv('../data/clean/simple_x_fm')
    y_simple = pd.read_csv('../data/clean/simple_y_fm')
    X_simple.reset_index()
    y_simple.reset_index()

    simple_X_train_mask = X_simple['year'] < 2014
    simple_X_test_mask = X_simple['year'] >= 2014
    simple_y_train_mask = y_simple['year'] < 2014
    simple_y_test_mask = y_simple['year'] >= 2014

    simple_X_train = X_simple[simple_X_train_mask].set_index('year')
    simple_X_test = X_simple[simple_X_test_mask].set_index('year')
    simple_y_train = y_simple[simple_y_train_mask].set_index('year')
    simple_y_test = y_simple[simple_y_test_mask].set_index('year')


    #Run Linear Regression
    simple_summery = summary_model(simple_X_train, simple_y_train, label='scatter')
    reg = LinearRegression().fit(simple_X_train,simple_y_train)
    reg.score(simple_X_train, simple_y_train)
    simple_y_pred = reg.predict(simple_X_test)
    print('MSE = ', mean_squared_error(simple_y_test,simple_y_pred))
    
    # Run Random Forest Regressor 

    rf_s = RandomForestRegressor(n_estimators=100, random_state=0,bootstrap = False)
    rf_s.fit(simple_X_train, simple_y_train.values.ravel())
    simple_y_pred = rf_s.predict(simple_X_test)

    simple_feat_importances = rf_s.feature_importances_
    simple_idx = np.argsort(rf_s.feature_importances_)[::-1]
    simple_features = ['BBLS','PSI']
    plot_feat_imp(simple_idx, simple_features, simple_feat_importances,  n = 2, fname = '../images/simple_rf_feature_importances.png')
    
    simple_test_values = simple_y_test.values
    simple_errors = abs(simple_y_pred - simple_test_values )
    
    # Calculate mean absolute percentage error (MAPE)
    simple_mape = np.mean(100 * (simple_errors / simple_test_values))

    # Calculate accuracy
    simple_accuracy = 100 - simple_mape

    print('Mean Absolute Error:', metrics.mean_absolute_error(simple_y_test.values.ravel(), simple_y_pred))
    print('Mean Squared Error:', metrics.mean_squared_error(simple_y_test.values.ravel(), simple_y_pred))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(simple_y_test.values.ravel(), simple_y_pred)))

    print('Metrics for Random Forest Trained on Simple Data')
    print('Average absolute error:', round(np.mean(simple_errors), 2), 'Earthquakes')
    print('Accuracy:', round(simple_accuracy, 2), '%.')


