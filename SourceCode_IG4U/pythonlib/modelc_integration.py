# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# import required module
'''import os, sys
loginlib = sys.path.append(os.path.join(os.path.dirname(__file__), "pythonlib"))
sys.path.insert(0, loginlib)'''
import pandas as pd
import sys
import os
sys.path.insert(0, './pythonlib')

from glob import glob
import numpy as np

import pickle


from sklearn.model_selection import RandomizedSearchCV, train_test_split

class prediction_mode:
        def __init__(self,df_profile,df_posts,profile):
            self.profile = profile
            self.df_profile = pd.DataFrame(df_profile)
            self.df_post = pd.DataFrame(df_posts)
            #self.df_topic_po = pd.DataFrame(df_topic_po)
            #self.df_topic_pro = pd.DataFrame(df_topic_pro)
            self.path = "./static/web/profile/"+self.profile
            
            

            
        def datamerge(self):
            df_post_new = self.df_post
            df_profile_new = self.df_profile
            #self.df_profile = pd.merge(self.df_profile,self.df_topic_pro, left_index=True, right_index=True)
            
            #self.df_post = pd.merge(self.df_post, self.df_topic_po, left_index=True, right_index=True)
            df_post_new.columns = 'PO_' + df_post_new.columns
            df_profile_new.columns = 'PRO_' + df_profile_new.columns
            #print(self.df_profile.columns)

            #print(self.df_post.columns)
            rowcount = len(self.df_post.index)
            
            newdf = pd.DataFrame(np.repeat(df_profile_new.values, rowcount, axis=0))
            newdf.columns = df_profile_new.columns
            df_profile_new = newdf
            
            #self.df_profile.head()
            BASE_DIR  = os.path.split(os.getcwd())[0]
            path = BASE_DIR+"/static/web/profile/"+self.profile
            
            
            filename_hash = 'rating_hashtag.sav'
            rating_hashtag = pickle.load(open('pythonlib/'+filename_hash, 'rb'))
            pred = rating_hashtag.predict(self.profile,'' )
            rating=[round(pred.est,2)]
            
            filename_tag = 'rating_tag_accounts.sav'
            filename_tag_acc = pickle.load(open('pythonlib/'+filename_tag, 'rb'))
            pred = filename_tag_acc.predict(self.profile,'' )
            rating.append(round(pred.est,2))
            
            with open(self.path+'/rating.csv', 'w') as fp:
                for item in rating:
                    # write each item on a new line
                    fp.write("%s\n" % item)
                fp.close()
                print('Done')
                    
            
            self.df_post_profile = df_post_new.join(df_profile_new)
            
            #self.df_post_profile.to_csv(self.path+"/Model_c_"+self.profile+".csv",index=False)
            #print(self.df_post_profile.columns)
            
            #print(self.df_post_profile.columns)
            #return self.df_post_profile
            self.dataprocess()
            
        def dataprocess(self):                       
            
            self.df_post_profile.rename(columns={'PO_PO_post_type':'PO_post_type',
            'PO_Year':'Year',
            'PO_tag_accounts':'PO_tag_accounts',
            'PO_Skincare_Treatment':'PO_Skincare_Treatment',
            'PO_Lifestyle_Health':'PO_Lifestyle_Health',
            'PO_Beauty_Makeup':'PO_Beauty_Makeup',
            'PO_Life_Happiness':'PO_Life_Happiness',
            'PO_neu':'PO_neu',
            'PO_Month':'Month',
            'PO_description_Emoji':'PO_description_Emoji',
            'PO_clean_text':'PO_clean_text',
            'PO_Work_Event':'PO_Work_Event',
            'PO_Shop_Business_Advertisement':'PO_Shop_Business_Advertisement',
            'PO_Travel_Celebrations':'PO_Travel_Celebrations',
            'PO_dominant_topic':'PO_dominant_topic',
            'PO_pos':'PO_pos',
            'PO_description_Language':'PO_description_Language_Freq',
            'PO_Hobby':'PO_Hobby',
            'PO_Fitness':'PO_Fitness',
            'PO_Food':'PO_Food',
            'PO_compound':'PO_compound',
            'PO_hashtag':'PO_hashtag',
            'PO_neg':'PO_neg',
            'PRO_PRO_media_count':'PRO_n_posts',
            'PRO_PRO_following_count':'PRO_following',
            'PRO_tag_accounts':'PRO_tag_accounts',
            'PRO_neu':'PRO_neu',
            'PRO_PRO_follower_count':'PRO_followers',
            'PRO_description_Emoji':'PRO_description_Emoji',
            'PRO_clean_text':'PRO_clean_text',
            'PRO_pos':'PRO_pos',
            'PRO_PRO_is_business':'PRO_is_business_account',
            'PRO_hashtag':'PRO_hashtag',
            'PRO_description_Language':'PRO_description_Language_Freq',
            'PRO_compound':'PRO_compound',
            'PO_PO_numbr_likes':'PO_numbr_likes','PO_PO_number_comments':'PO_number_comments'}, inplace=True)
            
            #print(self.df_post_profile.columns)
            self.df_post_profile = self.df_post_profile.drop(['PO_PO_URL',
            'PO_description_Translated',
            'PO_PO_description',
            'PO_description',
            'PO_PO_number_view_count',
            'PO_description',
            'PRO_PRO_pk',
            'PRO_PRO_username',
            'PRO_PRO_is_private',
            'PRO_PRO_profile_pic_url_hd',
            'PRO_PRO_external_url',
            'PRO_PRO_category',
            'PRO_description_Translated',
            'PRO_Skincare_Treatment',
            'PRO_Lifestyle_Health',
            'PRO_Beauty_Makeup',
            'PRO_Life_Happiness',
            'PRO_PRO_full_name',
            'PRO_PRO_profile_pic_url',
            'PRO_PRO_is_verified',
            'PRO_PRO_description',
            'PRO_PRO_account_type',
            'PRO_description',
            'PRO_Work_Event',
            'PRO_Shop_Business_Advertisement',
            'PRO_Travel_Celebrations',
            'PRO_dominant_topic',
            'PRO_Hobby',
            'PRO_Fitness',
            'PRO_Food',
            'PRO_polarity','PO_polarity'], axis=1)
            
            self.df_post_profile['LOC_aj_exact_city_match']=0
            self.df_post_profile['LOC_aj_exact_country_match']=0
            self.df_post_profile['LOC_lat']=0
            self.df_post_profile['LOC_lng']=0
            self.df_post_profile['neu']=0
            self.df_post_profile['LOC_cd_Freq']=0
            self.df_post_profile['LOC_slug_Freq']=0
            self.df_post_profile['points']=0
            self.df_post_profile['points_C']=0
                        
            PRO_is_business_account = pd.Categorical(pd.Categorical(self.df_post_profile['PRO_is_business_account']).codes)
            self.df_post_profile['PRO_is_business_account'] = PRO_is_business_account
            
            self.df_post_profile.PRO_clean_text = self.df_post_profile.PRO_clean_text.fillna('')
            self.df_post_profile.PO_clean_text = self.df_post_profile.PO_clean_text.fillna('')
            
            
            self.df_post_profile.PO_hashtag = self.df_post_profile.PO_hashtag.fillna('')
            
            self.df_post_profile.PO_tag_accounts = self.df_post_profile.PO_tag_accounts.fillna('')
            
            self.df_post_profile.PO_description_Emoji = self.df_post_profile.PO_description_Emoji.fillna('')
            
            self.df_post_profile.PRO_description_Emoji = self.df_post_profile.PRO_description_Emoji.fillna(self.df_post_profile['PO_description_Emoji'])
            
            self.df_post_profile.PRO_hashtag = self.df_post_profile.PRO_hashtag.fillna(self.df_post_profile['PO_hashtag'])
            
            
            self.df_post_profile.PRO_tag_accounts = self.df_post_profile.PRO_tag_accounts.fillna(self.df_post_profile['PO_tag_accounts'])
            
            
            self.df_post_profile['PRO_hashtag'] = self.df_post_profile['PRO_hashtag'].str.split().str.len()
            self.df_post_profile['PO_hashtag'] = self.df_post_profile['PO_hashtag'].str.split().str.len()
            
            
            self.df_post_profile['PRO_tag_accounts'] = self.df_post_profile['PRO_tag_accounts'].str.split().str.len()
            self.df_post_profile['PO_tag_accounts'] = self.df_post_profile['PO_tag_accounts'].str.split().str.len()
            
            
            self.df_post_profile['PRO_description_Emoji'] = self.df_post_profile.PRO_description_Emoji.str.strip().str.split(',').apply(len)
            self.df_post_profile['PO_description_Emoji'] = self.df_post_profile.PO_description_Emoji.str.strip().str.split(',').apply(len)
            
            self.df_post_profile['PRO_clean_text'] = self.df_post_profile['PRO_clean_text'].str.split().str.len()
            self.df_post_profile['PO_clean_text'] = self.df_post_profile['PO_clean_text'].str.split().str.len()
            
            self.df_post_profile.PRO_hashtag = self.df_post_profile.PRO_hashtag.fillna('0')
            self.df_post_profile.PO_hashtag = self.df_post_profile.PO_hashtag.fillna('0')
            
            self.df_post_profile.PRO_tag_accounts = self.df_post_profile.PRO_tag_accounts.fillna('0')
            self.df_post_profile.PO_tag_accounts = self.df_post_profile.PO_tag_accounts.fillna('0')
            
            self.df_post_profile.PRO_description_Emoji = self.df_post_profile.PRO_description_Emoji.fillna('0')
            self.df_post_profile.PO_description_Emoji = self.df_post_profile.PO_description_Emoji.fillna('0')
            
            
            self.df_post_profile['PRO_description_Language_Freq'] = self.df_post_profile.groupby('PRO_description_Language_Freq')['PRO_description_Language_Freq'].transform('count')
            self.df_post_profile['PO_description_Language_Freq'] = self.df_post_profile.groupby('PO_description_Language_Freq')['PO_description_Language_Freq'].transform('count')
            
            
            
            self.df_post_profile = self.df_post_profile.replace(r'^\s*$', 0, regex=True)
            
            self.df_post_profile = self.df_post_profile.replace(np.nan, 0, regex=True)
            self.outliers_page()
            
        def outliers_page(self):
                  
            columns = list(self.df_post_profile.columns)
            columns.remove('Year')
            columns.remove('Month')
            #columns.remove('PO_clean_text')
            #columns.remove('PO_description_Emoji')
            #columns.remove('PRO_clean_text')
            #columns.remove('PRO_description_Emoji')
            columns.remove('PRO_is_business_account')
            columns.remove('LOC_aj_exact_city_match')
            columns.remove('LOC_aj_exact_country_match')
            columns.remove('PO_post_type')
            #columns.remove('PO_number_comments')
            #columns.remove('PO_numbr_likes')
            columns.remove('PO_dominant_topic')
            columns.remove('PO_Food')
            columns.remove('PO_Work_Event')
            columns.remove('PO_Lifestyle_Health')
            columns.remove('PO_Fitness')
            columns.remove('PO_Travel_Celebrations')
            columns.remove('PO_Hobby')
            columns.remove('PO_Beauty_Makeup')
            columns.remove('PO_Skincare_Treatment')
            columns.remove('PO_Life_Happiness')
            columns.remove('PO_Shop_Business_Advertisement')
            
            for i in columns:
                #print(i)
                upper_limit = self.df_post_profile[i].quantile(0.888)
                lower_limit = self.df_post_profile[i].quantile(0.01)
                self.df_post_profile[i] = np.where(
                self.df_post_profile[i]>upper_limit,
                upper_limit,
                np.where(
                    self.df_post_profile[i]<lower_limit,
                    lower_limit,
                    self.df_post_profile[i]))
                
            columns = ['PO_clean_text','PO_description_Emoji','PRO_clean_text','PRO_description_Emoji']
            
            upper_limit = self.df_post_profile['PRO_followers'].quantile(0.75)
            lower_limit = self.df_post_profile['PRO_followers'].quantile(0.01)
            
            for i in columns:
                upper_limit = self.df_post_profile[i].mean() + 3*self.df_post_profile[i].std()
                lower_limit = self.df_post_profile[i].mean() - 3*self.df_post_profile[i].std()
                self.df_post_profile[i] = np.where(
                self.df_post_profile[i]>upper_limit,
                upper_limit,
                np.where(
                    self.df_post_profile[i]<lower_limit,
                    lower_limit,
                    self.df_post_profile[i]))
            
            
            #self.df_post_profile['points'] = self.df_post_profile.apply(self.pointtable, axis = 1)
            
            self.df_post_profile['points_C'] = self.df_post_profile.apply(self.pointtableC, axis = 1)
            self.prediction()
            
        def prediction(self):
            #self.datamerge()
            X = self.df_post_profile[['PO_post_type', 'PRO_following', 'PRO_followers', 'PRO_n_posts',
            'PRO_is_business_account', 'LOC_aj_exact_city_match',
            'LOC_aj_exact_country_match', 'LOC_lat', 'LOC_lng', 'PRO_hashtag',
            'PRO_tag_accounts', 'PO_hashtag', 'PO_tag_accounts',
            'PRO_description_Emoji', 'PO_description_Emoji', 'PO_clean_text',
            'PRO_clean_text', 'PO_Food', 'PO_Work_Event', 'PO_Lifestyle_Health',
            'PO_Fitness', 'PO_Travel_Celebrations', 'PO_Hobby', 'PO_Beauty_Makeup',
            'PO_Skincare_Treatment', 'PO_Life_Happiness',
            'PO_Shop_Business_Advertisement', 'PO_dominant_topic', 'PO_neg', 'neu',
            'PO_pos', 'PO_compound', 'PRO_neg', 'PRO_pos', 'PRO_compound', 'Year',
            'Month', 'PO_neu', 'LOC_cd_Freq', 'LOC_slug_Freq',
            'PRO_description_Language_Freq', 'PO_description_Language_Freq',
            'points_C']]
            filename_name = 'model_likes.pkl'
            #model_likes = pickle.load(open('pythonlib/'+filename_name, 'rb'))
            model_likes = pickle.load(open('pythonlib/'+filename_name, 'rb'))
            self.df_post_profile['y_likes_pred'] = pd.DataFrame(model_likes.predict(X))
            
            filename_comments = 'model_comments.pkl'
            #model_comments = pickle.load(open('pythonlib/'+filename_comments, 'rb'))
            model_comments = pickle.load(open('pythonlib/'+filename_comments, 'rb'))
            self.df_post_profile['y_comments_pred'] = pd.DataFrame(model_comments.predict(X))    
            
            
            
            
            
            
            
            self.df_post_profile['y_likes_pred'] = self.df_post_profile['y_likes_pred'].round()
            self.df_post_profile['y_comments_pred'] = self.df_post_profile['y_comments_pred'].round()

            
            
            
            BASE_DIR  = os.path.split(os.getcwd())[0]
            path = "./static/web/profile/"+self.profile
            self.df_post_profile.to_csv(path+"/Model_c_"+self.profile+".csv",index=False)
            
            #return self.df_post_profile
            
        def pointtable(self,features):
            points =0
            
            if features['PO_compound'] >= 0 and features['PRO_n_posts'] > 20 and features['PRO_followers']>100 and features['PO_numbr_likes'] > 10 and  features['PO_number_comments'] > 5 :
                    points =  0.1
        
            if features['PO_compound'] >= 0 and features['PRO_n_posts'] > 50 and features['PRO_followers']>200 and features['PO_numbr_likes'] > 10 and  features['PO_number_comments'] > 10 :
                    points =  0.2
        
            if features['PO_compound'] >= 0 and features['PRO_n_posts'] > 200 and features['PRO_followers']>1000 and features['PO_numbr_likes'] > 50 and  features['PO_number_comments'] > 20 :
                    points =  0.3
        
            if features['PO_compound'] >= 0 and features['PRO_n_posts'] > 500 and features['PRO_followers']>1000 and features['PO_numbr_likes'] > 100 and  features['PO_number_comments'] > 50 :
                    points =  0.4
        
            if features['PO_compound'] >= 0 and features['PRO_n_posts'] > 1000 and features['PRO_followers']>2000 and features['PO_numbr_likes'] > 1000 and  features['PO_number_comments'] > 100 :
                    points =  0.5
        
            if features['PO_compound'] >= 0 and features['PRO_n_posts'] > 1000 and features['PRO_followers']>10000 and features['PO_numbr_likes'] > 10000 and  features['PO_number_comments'] > 200 :
                    points =  0.6
        
            if features['PO_compound'] >= 0 and features['PRO_n_posts'] > 2000 and features['PRO_followers']>100000 and features['PO_numbr_likes'] > 100000 and  features['PO_number_comments'] > 1000 :
                    points =  0.8
        
            if features['PO_compound'] < 0 and features['PRO_n_posts'] > 50 and features['PRO_followers']>50:
                    points =  -0.2
        
            if features['PO_compound'] < 0 and features['PRO_n_posts'] > 500 and features['PRO_followers']>1000:
                    points = 0.5
        
            if features['PRO_is_business_account'] == 1:
                    points = points  * 1.2
            
            return points
        
        def pointtableC(self,features):
            points =0
            weight = (features['PO_compound'] + features['PRO_compound'])/2
            
            if features['PRO_n_posts'] > 10 and features['PRO_followers']>20 and features['PO_numbr_likes'] > 5 and  features['PO_number_comments'] > 3 and  features['PRO_following'] > 5 :
                    points =  0.05 * (1 + weight)
        
            if features['PRO_n_posts'] > 15 and features['PRO_followers']>50 and features['PO_numbr_likes'] > 8 and  features['PO_number_comments'] > 4 and  features['PRO_following'] > 10 :
                    points =  0.1 * (1 + weight)
        
            if features['PRO_n_posts'] > 20 and features['PRO_followers']>100 and features['PO_numbr_likes'] > 10 and  features['PO_number_comments'] > 5 and  features['PRO_following'] > 20 :
                    points =  0.15 * (1 + weight)
        
            if features['PRO_n_posts'] > 50 and features['PRO_followers']>200 and features['PO_numbr_likes'] > 20 and  features['PO_number_comments'] > 10 and  features['PRO_following'] > 50 :
                    points =  0.2 * (1 + weight)
        
            if features['PRO_n_posts'] > 200 and features['PRO_followers']>1000 and features['PO_numbr_likes'] > 50 and  features['PO_number_comments'] > 20 and  features['PRO_following'] > 100 :
                    points =  0.3 * (1 + weight)
        
            if features['PRO_n_posts'] > 500 and features['PRO_followers']>1000 and features['PO_numbr_likes'] > 100 and  features['PO_number_comments'] > 50 and  features['PRO_following'] > 500 :
                    points =  0.4 * (1 + weight)
        
            if features['PRO_n_posts'] > 1000 and features['PRO_followers']>2000 and features['PO_numbr_likes'] > 1000 and  features['PO_number_comments'] > 100 and  features['PRO_following'] > 500 :
                    points =  0.5 * (1 + weight)
        
            if features['PRO_n_posts'] > 1000 and features['PRO_followers']>10000 and features['PO_numbr_likes'] > 10000 and  features['PO_number_comments'] > 200 and  features['PRO_following'] > 500 :
                    points =  0.6 * (1 + weight)
        
            if features['PRO_n_posts'] > 2000 and features['PRO_followers']>100000 and features['PO_numbr_likes'] > 100000 and  features['PO_number_comments'] > 1000 and  features['PRO_following'] > 500 :
                    points =  0.8 * (1 + weight)
        
            if features['PRO_is_business_account'] == 1:
                    points = points  * 1.2
            
            return points



''' 
                          
profile='archieplutowaggingtails'
BASE_DIR  = os.path.split(os.getcwd())[0]
path = BASE_DIR+"/static/web/profile/"+profile

df_profile= pd.read_csv(path+"/"+os.path.basename(glob(path+"/PRO_*.csv")[0]))
df_post= pd.read_csv(path+"/"+os.path.basename(glob(path+"/PO_*.csv")[0]))

df_topic_po= pd.read_csv(path+"/"+os.path.basename(glob(path+"/TM_po_*.csv")[0]))
df_topic_pro= pd.read_csv(path+"/"+os.path.basename(glob(path+"/TM_pro_*.csv")[0]))

df_profile = pd.merge(df_profile,df_topic_pro, left_index=True, right_index=True)

df_post = pd.merge(df_post, df_topic_po, left_index=True, right_index=True)





modelc =prediction_mode(df_profile,df_post,profile)
modelc.datamerge()

df_model_c= pd.read_csv(path+"/"+os.path.basename(glob(path+"/Model_c_*.csv")[0]))
 
#X = X.drop(['PO_numbr_likes', 'PO_number_comments'], axis=1)
     
y_likes = df_post_profile.PO_numbr_likes
y_comments = df_post_profile.PO_number_comments

df_modelc= pd.read_csv(path+"/"+os.path.basename(glob(path+"/Model_c_*.csv")[0]))'''