#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 20:06:04 2023

@author: saurav
"""



import pandas as pd
import numpy as np
import nltk
import re
#from nltk.corpus import stopwords
#from nltk.corpus import wordnet
#from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import demoji
demoji.download_codes()
from translate import Translator
from langdetect import detect
#from datetime import datetime
import os
#import glob
#import csv
import pickle
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

my_stopwords = nltk.corpus.stopwords.words('english')
word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem
my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@#'

class Topic_Sentiment_modeling_PO:
     def __init__(self,df,profile,po_pro_type):
         self.df = pd.DataFrame(df)
         self.df =  self.df.rename(columns={self.df.columns[0]: 'description'})
         self.profile = profile
         self.po_pro_type = po_pro_type
         BASE_DIR  = os.path.split(os.getcwd())[0]
         self.path = "./static/web/profile/"+self.profile
         #self.path =BASE_DIR+ "/static/web/profile/"+self.profile
         #self.description_processing()
         #self.df['description_Translated'].apply(lambda x: x if x is not None else "")

    
     def description_processing(self):
        Emoji_list = []
        x=[]
        Translated=[]
        
        self.df['hashtag'] = self.df.description.str.extractall('(#\w+)').groupby(level=0 ,group_keys=True)[0].apply(' '.join)
        self.df['tag_accounts'] =self.df.description.str.extractall('(@\w+)').groupby(level=0,group_keys=True)[0].apply(' '.join)
        #print(self.df['hashtag'] )
                 
        self.df.hashtag = self.df.hashtag.fillna('')
        self.df.tag_accounts = self.df.tag_accounts.fillna('')
        self.df.description = self.df.description.fillna('')
        for raw_sentence in self.df['description']:
            #print(raw_sentence)
           
            Emoji_list.append(', '.join(list(demoji.findall(str(raw_sentence)).values())))
            #print(Emoji_list)
            raw_sentence = raw_sentence.encode('ascii', 'ignore').decode('ascii')
            try:
                x.append(detect(raw_sentence))
            except:
                x.append('Unknown')
            translator = Translator(to_lang='en')
            translation = translator.translate(raw_sentence)
            Translated.append(translation)
            #print(Translated)
        
        self.df['description_Emoji']= Emoji_list
        self.df['description_Language']= x
        self.df['description_Translated']= Translated
        

        self.df.description_Translated = self.df.description_Translated.fillna("")
        self.df.hashtag = self.df.hashtag.fillna("")
        self.df.tag_accounts = self.df.tag_accounts.fillna("")
        
        #print(self.df.description_Translated)
        self.df['clean_text'] = self.df.description_Translated.apply(self.clean_tweet)

        topicnames = self.topic_modelling()
        self.sentiment_analysis()
        self.df.to_csv(self.path+"/TM_"+self.po_pro_type+"_"+self.profile+".csv",index=False)
        with open(self.path+"/Topic_"+self.po_pro_type+"_"+self.profile+".csv", 'w') as f:
            for line in topicnames:
                f.write(f"{line},")
        
        return self.df,topicnames


     def topic_modelling(self):
        no_top_words = 1
        number_of_topics = 10
        vectorizer = CountVectorizer(token_pattern='\w+|\$[\d\.]+|\S+')
        tf = vectorizer.fit_transform(self.df['clean_text']).toarray()
        tf_feature_names = vectorizer.get_feature_names_out()
        loaded_model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)
        lda_output = loaded_model.fit_transform(tf)
        Topics = display_topics(loaded_model, tf_feature_names, no_top_words)
        Topics_list = Topics.values.tolist()[0]
        indexes = [0, 2, 4, 6, 8 ,10, 12, 14, 16, 18]
        Topics_list = [Topics_list[x] for x in indexes]
        Topics_list = list(dict.fromkeys(Topics_list))
        
        no_top_words = 10
        number_of_topics = 10
        filename = 'Topic_model_Pickle.sav'
        loaded_model = pickle.load(open('pythonlib/'+filename, 'rb'))
        #loaded_model = pickle.load(open(filename, 'rb'))
        
        filename = 'vectorizer_Pickle.sav'
        vectorizer = pickle.load(open('pythonlib/'+filename, 'rb'))
        #vectorizer = pickle.load(open(filename, 'rb'))
        topicnames= []
        try:
            tf = vectorizer.transform(self.df['clean_text']).toarray()
            tf_feature_names = vectorizer.get_feature_names_out()
            lda_output = loaded_model.transform(tf)
            
            
            for i in range(number_of_topics):
            
                if i==0:
                    topicnames.append('Hobby')
                if i== 1:
                    topicnames.append('Skincare_Treatment')
                if i== 2:
                    topicnames.append('Work_Event')
                if i== 3:
                    topicnames.append('Fitness')
                if i== 4:
                    topicnames.append('Lifestyle_Health')
                if i== 5:
                    topicnames.append('Shop_Business_Advertisement')
                if i== 6:
                    topicnames.append('Beauty_Makeup')
                if i== 7:
                    topicnames.append('Travel_Celebrations')
                if i== 8:
                    topicnames.append('Food')
                if i== 9:
                    topicnames.append('Life_Happiness')
            
        except:
            for i in len(Topics_list):
                topicnames.append(Topics_list[i])

              
                
        #topicnames = ["Topic" + str(i) for i in range(no_top_words)]
        
        # index names
        docnames = ["Doc" + str(i) for i in range(len(self.df))]
        
        # Make the pandas dataframe
        df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)
        
        # Get dominant topic for each document
        dominant_topic = np.argmax(df_document_topic.values, axis=1)
        
        dict_map = {0:'Hobby',1:'Skincare_Treatment',2:'Work_Event',3:'Fitness',4:'Lifestyle_Health',5:'Shop_Business_Advertisement',6:'Beauty_Makeup',7:'Travel_Celebrations',8:'Food',9:'Life_Happiness'}
        
        dict_remap = {'Hobby':5,'Skincare_Treatment':7,'Work_Event':1,'Fitness':3,'Lifestyle_Health':2,'Shop_Business_Advertisement':9,'Beauty_Makeup':6,'Travel_Celebrations':4,'Food':0,'Life_Happiness':8}
        
        
        #'PO_Topic0': 'PO_Food', 'PO_Topic1': 'PO_Work_Event', 'PO_Topic2': 'PO_Lifestyle_Health', 'PO_Topic3': 'PO_Fitness', 'PO_Topic4': 'PO_Travel_Celebrations', 'PO_Topic5': 'PO_Hobby', 'PO_Topic6': 'PO_Beauty_Makeup', 'PO_Topic7': 'PO_Skincare_Treatment', 'PO_Topic8': 'PO_Life_Happiness', 'PO_Topic9': 'PO_Shop_Business_Advertisement'})
        
        df_document_topic['dominant_topic'] = dominant_topic
        
        updateSer = df_document_topic['dominant_topic'].map(dict_map)
        #print(updateSer)
        df_document_topic['dominant_topic'] = updateSer
        
        updateSer_remap = df_document_topic['dominant_topic'].map(dict_remap)
        df_document_topic['dominant_topic'] = updateSer_remap
        #print(updateSer_remap)
        
        # Styling
        def color_green(val):
            color = 'green' if val > .1 else 'black'
            return 'color: {col}'.format(col=color)
        
        def make_bold(val):
            weight = 700 if val > .1 else 400
            return 'font-weight: {weight}'.format(weight=weight)
        
        
        # Apply Style
        df_document_topics = df_document_topic.head(15).style.applymap(color_green).applymap(make_bold)
        
        df_document_topic = df_document_topic.reset_index(drop = True)
        
        df_document_topics 
        
        self.df = self.df.join(df_document_topic)
        
        return Topics_list
        
     def sentiment_analysis(self):
         analyzer = SentimentIntensityAnalyzer()
         self.df['polarity'] = self.df['clean_text'].apply(lambda x: analyzer.polarity_scores(x))
         self.df = pd.concat([self.df, self.df['polarity'].apply(pd.Series)], axis=1)

     def deEmojify(self,inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')
    
     def rem_en(self,input_txt):
        words = input_txt.lower().split()
        noise_free_words = [word for word in words if word not in my_stopwords] 
        noise_free_text = " ".join(noise_free_words) 
        return noise_free_text
    
     def remove_links(self,insta):
        '''Takes a string and removes web links from it'''
        insta = re.sub(r'http\S+', '', insta) # remove http links
        insta = re.sub(r'bit.ly/\S+', '', insta) # rempve bitly links
        insta = insta.strip('[link]') # remove [links]
        insta = re.sub(r'\\', '', insta) # remove http links
        return insta
    
     def remove_users(self,insta):
        '''Takes a string and removes retweet and @user information'''
        insta = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', str(insta)) # remove retweet
        insta = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', str(insta)) # remove tweeted at
        return insta
    
     # cleaning master function
     def clean_tweet(self,insta, bigrams=False):
        #print(insta)
        insta = self.remove_users(insta)
        insta = self.remove_links(insta)
        insta = self.deEmojify(insta)
        insta = self.rem_en(insta)
        insta = insta.lower() # lower case
        insta = re.sub('['+my_punctuation + ']+', ' ', insta) # strip punctuation
        insta = re.sub('\s+', ' ', insta) #remove double spacing
     
        insta = re.sub('([0-9]+)', '', insta) # remove numbers
        insta = re.sub(r'\b\w{1,3}\b', '', insta)
        insta_token_list = [word for word in insta.split(' ')
                                if word not in my_stopwords] # remove stopwords
    
        insta_token_list = [word_rooter(word) if '#' not in word else word
                            for word in insta_token_list] # apply word rooter
        if bigrams:
            insta_token_list = insta_token_list+[insta_token_list[i]+'_'+insta_token_list[i+1]
                                                for i in range(len(insta_token_list)-1)]
        insta = ' '.join(insta_token_list)
        return insta

def display_topics(model, feature_names, no_top_words):
    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict["Topic %d words" % (topic_idx)]= ['{}'.format(feature_names[i])
                        for i in topic.argsort()[:-no_top_words - 1:-1]]
        topic_dict["Topic %d weights" % (topic_idx)]= ['{:.1f}'.format(topic[i])
                        for i in topic.argsort()[:-no_top_words - 1:-1]]
    return pd.DataFrame(topic_dict)


'''

from glob import glob
profile='archieplutowaggingtails'
BASE_DIR  = os.path.split(os.getcwd())[0]
path = BASE_DIR+"/static/web/profile/"+profile


df_posts= pd.read_csv(path+"/"+os.path.basename(glob(path+"/PO_*.csv")[0]))


Topic_modelling  = Topic_Sentiment_modeling_PO(df_posts['PO_description'],profile,'po')
tm = Topic_modelling.description_processing()

df_modelc= pd.read_csv(path+"/"+os.path.basename(glob(path+"/Model_c_*.csv")[0]))
#df_tp = tm[0]
#Topics_list = tm[1]

from glob import glob
profile='doggodorable'
BASE_DIR  = os.path.split(os.getcwd())[0]
path = BASE_DIR+"/static/web/profile/"+profile


df_posts= pd.read_csv(path+"/"+os.path.basename(glob(path+"/PRO_*.csv")[0]))
df_posts.PRO_description = df_posts.PRO_description.fillna(df_posts['PRO_full_name'])
Topic_modelling  = Topic_Sentiment_modeling(df_posts['PRO_description'],profile,'pro')
tm = Topic_modelling.description_processing()
df_tp = tm[0]
Topics_list = tm[1]
'''
