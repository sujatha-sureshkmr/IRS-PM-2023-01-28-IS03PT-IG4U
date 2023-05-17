#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 11:39:13 2023

@author: saurav
"""


#import instaloader
import pandas as pd
import numpy as np
import os
from itertools import islice
from math import ceil
from PIL import Image
import requests
from io import BytesIO
from Topic_Modeling import Topic_Sentiment_modeling
#from Topic_Modeling_PO import Topic_Sentiment_modeling_PO
#from instaloader import Instaloader, Profile
import time
from instagrapi import Client



class instagramapi:
   def __init__(self,Insta_username):
       self.USER=['bjsz.nus@gmail.com','nus.project.group.bjsz@gmail.com','IG4YouBryan1@gmail.com','IG4YouBryan2@gmail.com','nus.ig.test.1@gmail.com','nus.project.ig4u.1@gmail.com']
       self.USERNAME = 'bjsz.nus@gmail.com'#'nus.project.group.bjsz@gmail.com'
       self.PASSWORD = 'wrCb729zH8rP'
       self.profile = Insta_username
       #profile = "pbakes_sg"
       BASE_DIR  = os.path.split(os.getcwd())[0]
       #self.path = BASE_DIR+"/static/web/profile/"+self.profile
       self.path = "./static/web/profile/"+self.profile
       isExist = os.path.exists(self.path)
       if not isExist:
          os.makedirs(self.path)
          os.makedirs(self.path+"/img")
         
   def instalogin(self):
       i=0
       self.medias = None
       while (i<=5) and (self.medias is None):
           try:
                print(i)
                print(self.medias,self.USER[i],self.profile)
                if i > 5:
                    break
                
                cl = Client()                
                cl.login(self.USER[i], self.PASSWORD)
                
                self.user_id = cl.user_id_from_username(self.profile)      
                self.medias = cl.user_medias(self.user_id,5000)
                #print(self.medias)
                self.user = cl.user_info_by_username(self.profile).dict()
                cl.logout()              
           except:
               i=i+1
               
               cl.logout()
               #profile='archieplutowaggingtails'
           
    
       cl.logout()
   
   def instaprofile(self):
       self.instalogin()
       df = pd.DataFrame.from_dict(self.user, orient='index')
        
       df_profile = df.T
        
       df_profile = df_profile.add_prefix('PRO_')
        
       df_profile = df_profile.drop(["PRO_public_email","PRO_contact_phone_number","PRO_public_phone_country_code","PRO_public_phone_number","PRO_business_contact_method","PRO_business_category_name","PRO_category_name","PRO_address_street","PRO_city_id","PRO_city_name","PRO_latitude","PRO_longitude","PRO_zip","PRO_instagram_location_id","PRO_interop_messaging_user_fbid"], axis=1)
        
       df_profile = df_profile.rename(columns={'PRO_biography': 'PRO_description'})
       
       
       newdf = pd.DataFrame(df_profile.values)
       newdf.columns = df_profile.columns
       df_profile = newdf
       response = requests.get(df_profile['PRO_profile_pic_url_hd'].item())
       img = Image.open(BytesIO(response.content))
       im1 = img.save(self.path+"/img/PRO_"+self.profile+".jpg")
       df_profile.to_csv(self.path+"/PRO_"+self.profile+".csv",index=False)
       
       df_profile['PRO_description'] = df_profile['PRO_description'].replace('',df_profile['PRO_full_name'][0])
       
       print(df_profile['PRO_description'])
       PRO_Topic_modelling  = Topic_Sentiment_modeling(df_profile['PRO_description'],self.profile,'pro')
       PRO_Topic_modelling.description_processing()
       
       self.instaposts()
    
   def instaposts(self):
       df = pd.DataFrame (self.medias)
       for i in df.columns:
        #print(i)
           col_name = df[i].str[0].unique()
           df = df.rename({i: col_name[0]}, axis=1) 
           df[col_name[0]] = df[col_name[0]].str[1]
            
       df['Year']=pd.DatetimeIndex(df['taken_at']).year
       df['Month']=pd.DatetimeIndex(df['taken_at']).month
       
       df = df.drop(['taken_at','code','play_count',"pk","id","image_versions2","product_type","location","user","comments_disabled","commenting_disabled_for_viewer","has_liked","accessibility_caption","usertags","sponsor_tags","video_url","video_duration","title","resources","clips_metadata"], axis=1)
       df = df.rename(columns={'media_type': 'PO_post_type', 'comment_count': 'PO_number_comments','thumbnail_url':'PO_URL', 'like_count': 'PO_numbr_likes', 'caption_text': 'PO_description', 'view_count': 'PO_number_view_count'})
       df.sort_values(by=['PO_numbr_likes', 'PO_number_comments','PO_number_view_count'], inplace=True, ascending=False)
       
       df.to_csv(self.path+"/PO_"+self.profile+".csv",index=False)
       
       print(df['PO_description'].shape)
       #df['PO_description'] = df.PO_description.fillna('')
       
       PO_Topic_modelling  = Topic_Sentiment_modeling(df['PO_description'],self.profile,'po')      
       print(df['PO_description'].shape)
       PO_Topic_modelling.description_processing() 
       time.sleep(20)
       df = df.reset_index(drop=True)
       
       df_top20 = df.head(20)
       
       for row in df_top20['PO_URL']:
           if row != None:
              response = requests.get(row)
              img = Image.open(BytesIO(response.content))
              im1 = img.save(self.path+"/img/"+'PO_'+str(i)+"_"+self.profile+".jpg")
           i=i+1
      
       time.sleep(5)
       
'''
instagram = instagramapi('archieplutowaggingtails')
df_profile = instagram.instalogin()'''

#df_profile = instagram.instaprofile()