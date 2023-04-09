import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.inspection import permutation_importance
import seaborn as sns
import matplotlib.pyplot as plt


models = [LinearRegression(), Ridge(), BayesianRidge(), SGDRegressor(),   # Linear Models
          RandomForestRegressor(), DecisionTreeRegressor(),               # Tree Models
          MLPRegressor(),                                                 # Neural Networks
          KNeighborsRegressor(n_neighbors = 30),                          # Nearest Neighbor Models
          SVR()]                                                          # Stochastic Gradient Descent Models


prt = pd.read_csv(r"data\politician_region_scores.csv")
X = prt[[
    'Type',
    'Gender',
    'Age',
    'Party',
    'Follower Count',
    'Bachelor\'s Degree or Higher Proportion',
    'Foreign Born Proportion',
    'Mean Income',
    'Median Age',
    'Median Income',
    'Racial Diversity (Simpson Index)',
    'Unemployment Rate (%)'  ####SPELLING IS WRONG IN FILE ON COMPUTER
]]
y = prt['toxicity_mean']


X_ohe = pd.get_dummies(X, columns = ['Type', 'Gender', 'Party'])
X_ohe_std = (X_ohe - np.mean(X_ohe))/np.std(X_ohe)
y_std = (y - np.mean(y)) / np.std(y)


num_features = 7

totals = {X_ohe.columns[i] : 0 for i in range(len(X_ohe.columns))}
model_importances = pd.DataFrame()

for m in models:
    m.fit(X_ohe_std, y_std)
    f = permutation_importance(m, X_ohe_std, y_std,
                           n_repeats = 30,
                           random_state = 0)
    imp_dict = {X_ohe.columns[i] : np.round(f.importances_mean[i], 3) for i in range(len(X_ohe.columns))}
    s_imp_dict = dict(sorted(imp_dict.items(), key = lambda item: item[1], reverse = True))
    
    for f in list(s_imp_dict.keys())[:10]:
        totals[f] += s_imp_dict[f]

    model_importances[str(m)] = list(imp_dict.values())


model_importances = model_importances.set_axis(list(X_ohe.columns))[[str(m) for m in models]]

model_importances.to_csv(r'data\model_importances.csv')

sorted_totals = dict(sorted(totals.items(), key = lambda item: item[1], reverse = True))

print(sorted_totals)

sns.set_style('darkgrid')
sns.barplot(x = list(sorted_totals.values()), y = list(sorted_totals.keys()), orient = 'h')

plt.title('Features Importances by Attribute')
plt.xlabel('Attribute')
plt.ylabel('Feature Importance Metric')
plt.show()
