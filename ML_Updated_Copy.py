# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 18:03:41 2019
@author: jrg5701
"""

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

def predictState(user_cat,user_maincat,user_usd_goal_real,user_days_elapsed,user_country,user_month_launched):

    df = pd.read_csv("kickstarter_2018_clean.csv")
    
    #adds row to end of datasheet, so user's data can be factorized along with rest of data
    row=[0,0,user_cat,user_maincat,0,0,0,0,0,"successful",0,user_country,0,0,user_usd_goal_real,user_days_elapsed,user_month_launched]
    df.loc[len(df)] = row
    
    useful = df[['category', 'main_category' ,'usd_goal_real','days_elapsed', 'state','country','month_launched']]
    mainFact,main = pd.factorize(useful.main_category)
    subFact,sub = pd.factorize(useful.category)
    
    #Adjust the subcategories to they are farth apart from subcategories of other main categories
    for x in range(331675):
        subFact[x]= subFact[x] + mainFact[x]*200
    
    useful['main_category_index'] = mainFact
    useful.main_category.astype('category').cat.codes
     
    useful['category_index'] = subFact
    useful.category.astype('category').cat.codes
    
    useful.state = pd.Categorical(useful.state)
    useful['state_index'] = useful.state.cat.codes
    useful.state.astype('category').cat.codes
    
    useful.country = pd.Categorical(useful.country)
    useful['country_index'] = useful.country.cat.codes
    useful.country.astype('category').cat.codes
    
    #creats a array of user's inputs
    user_inputs=[[user_usd_goal_real, user_days_elapsed,useful.country_index[331674],user_month_launched,mainFact[331674],subFact[331674]]]
    #removes last row so user's input does not get user in training the model
    useful.drop(df.tail(1).index,inplace=True)
    
    factor = useful[['usd_goal_real', 'days_elapsed','country_index','month_launched','main_category_index','category_index']]
    outcome = useful[['state_index']]
    
    X_train, X_test, y_train, y_test = train_test_split(factor, outcome, test_size=.30)
    
    k = 9
    
    # train model
    neigh = KNeighborsClassifier(n_neighbors = k).fit(X_train, y_train)
    
    result = neigh.predict(X_test)
    
    #predicts the accuray
    train_compare = metrics.accuracy_score(y_train, neigh.predict(X_train))
    test_compare = metrics.accuracy_score(y_test, result)
    #print('Train accuracy = ', train_compare)
    #print('Test accuracy = ', test_compare)
    
    #
    result = neigh.predict(user_inputs)
    
    if(result == 0):
        return "Failed"
    else:
        return"Successful"
    
    #user_cat,user_maincat,user_usd_goal_real,user_days_elapsed,country,user_month_launched):
    #predictState("Illustration","Art",20,9,"US",4)