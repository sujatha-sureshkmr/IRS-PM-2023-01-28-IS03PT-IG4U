#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 20:57:43 2023

@author: saurav
"""

import numpy as np
import pandas as pd


# affinity propagation clustering
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import AffinityPropagation
from matplotlib import pyplot

from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate
import numpy as np
import pandas as pd

import pandas as pd
import pickle
'''
path='/home/saurav/Documents/NUS-Sem1/Project/Combined_Processed/Final'


appended_data = pd.read_csv(path+'/Post_Processed_Combined_relevant_columns.csv',sep=',',header=0, encoding='utf-8',error_bad_lines=False, engine="python")

'''

''' Hashtags '''
appended_data = appended_data[(appended_data["PRO_followers"] > 0)]
appended_data['Impressions'] = (appended_data['PO_numbr_likes']+appended_data['PO_number_comments'])*100/appended_data['PRO_followers'] 

 

hashtags_recommended = appended_data[['PO_dominant_topic','PO_hashtag','Impressions']]

dominant_topic_names = {0 : "Food",
                 1 : "Work_Event",
                 2 : "Lifestyle_Health",
                 3 : "Fitness",
                 4 : "Travel_Celebrations",
                 5 : "Hobby",
                 6 : "Beauty_Makeup",
                 7 : "Skincare_Treatment",
                 8 : "Life_Happiness",
                 9 : "Shop_Business_Advertisement"}

hashtags_recommended['PO_dominant_topic'] = hashtags_recommended["PO_dominant_topic"].map(dominant_topic_names)

hashtags_recommended = hashtags_recommended.dropna()

df = pd.melt(hashtags_recommended, id_vars=["PO_dominant_topic", "Impressions"], 
             value_name="PO_hashtag").drop(['variable'],axis=1).sort_values('PO_dominant_topic')

df2 = hashtags_recommended.PO_hashtag.str.split(' ').apply(pd.Series)  
df2.index = pd.MultiIndex.from_arrays(hashtags_recommended[['PO_dominant_topic', 'Impressions']].values.T, names=['PO_dominant_topic', 'Impressions'])
df2 = df2.stack().reset_index()
df1=df2[["PO_dominant_topic", "Impressions",0]]
df1 = df1.rename(columns={0: "PO_hashtags"})
df1 = df1[['PO_dominant_topic',"PO_hashtags","Impressions"]]


reader = Reader(rating_scale=(0,10))
data = Dataset.load_from_df(df1, reader)

trainset = data.build_full_trainset()  # use all data (ie no train/test split)

algo = KNNWithMeans(k=40,sim_options={'name': 'pearson'})

algo.fit(trainset) # build the model

filename = 'rating_hashtag.sav'
pickle.dump(algo, open(filename, 'wb'))


'''    

genes = df1['PO_dominant_topic'].unique()
for gene in genes:
    outfilename = gene + '_Hashtag.csv'
    print(outfilename)
    df1[df1['PO_dominant_topic'] == gene].to_csv(outfilename)
    
'''    
''' tag_accounts '''

tag_accounts_recommended = appended_data[['PO_dominant_topic','PO_tag_accounts','Impressions']]

dominant_topic_names = {0 : "Food",
                 1 : "Work_Event",
                 2 : "Lifestyle_Health",
                 3 : "Fitness",
                 4 : "Travel_Celebrations",
                 5 : "Hobby",
                 6 : "Beauty_Makeup",
                 7 : "Skincare_Treatment",
                 8 : "Life_Happiness",
                 9 : "Shop_Business_Advertisement"}

tag_accounts_recommended['PO_dominant_topic'] = tag_accounts_recommended["PO_dominant_topic"].map(dominant_topic_names)

tag_accounts_recommended = tag_accounts_recommended.dropna()

df = pd.melt(tag_accounts_recommended, id_vars=["PO_dominant_topic", "Impressions"], 
             value_name="PO_tag_accounts").drop(['variable'],axis=1).sort_values('PO_dominant_topic')

df2 = tag_accounts_recommended.PO_tag_accounts.str.split(' ').apply(pd.Series)  
df2.index = pd.MultiIndex.from_arrays(tag_accounts_recommended[['PO_dominant_topic', 'Impressions']].values.T, names=['PO_dominant_topic', 'Impressions'])
df2 = df2.stack().reset_index()
df1=df2[["PO_dominant_topic", "Impressions",0]]
df1 = df1.rename(columns={0: "PO_tag_accounts"})
df1 = df1[['PO_dominant_topic',"PO_tag_accounts","Impressions"]]


'''    
genes = df1['PO_dominant_topic'].unique()
for gene in genes:
    outfilename = gene + '_tag_accounts.csv'
    print(outfilename)
    df1[df1['PO_dominant_topic'] == gene].to_csv(outfilename)
    '''    

reader = Reader(rating_scale=(0,10))
data = Dataset.load_from_df(df1, reader)

trainset = data.build_full_trainset()  # use all data (ie no train/test split)

algo = KNNWithMeans(k=40,sim_options={'name': 'pearson'})

algo.fit(trainset) # build the model

filename = 'rating_tag_accounts.sav'
pickle.dump(algo, open(filename, 'wb'))

    
'''



reader = Reader(rating_scale=(0,10))
data = Dataset.load_from_df(df1, reader)

trainset = data.build_full_trainset()  # use all data (ie no train/test split)

algo = KNNWithMeans(k=40,sim_options={'name': 'pearson'})

algo.fit(trainset) # build the model

filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))


rawuid = 'archieplutowaggingtails' 
rawiid = '#dope' # was rated by Toby
test=1346

pred = algo.predict(rawuid, rawiid,test)
pred.est  
uid = trainset.to_inner_uid(rawuid)
iid = trainset.to_inner_iid(rawiid)
print("inner ids:","user=",uid,"item=",iid)

realrating = dict(trainset.ur[uid])[iid]; realrating  # retrieve the real rating
pred = algo.predict(rawuid, rawiid, r_ui = realrating, verbose = True)
pred



df3=df1.groupby(['PO_dominant_topic','PO_hashtags'])['PO_numbr_likes'+'PO_number_comments'].nlargest(10)
asd = len(appended_data[(appended_data["Impressions"]=="0")])'''

