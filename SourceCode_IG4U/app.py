from flask import Flask, render_template, redirect, url_for, request, flash
#from Login_Registration import userauthentication
import plotly.express as px
'''import os, sys
loginlib = sys.path.append(os.path.join(os.path.dirname(__file__), "pythonlib"))
sys.path.insert(0, loginlib)'''
import calendar
from pathlib import Path
import sys
import os
import numpy as np
sys.path.insert(0, './pythonlib')
instagram_page = "archieplutowaggingtails"
from Login_Registration import userauthentication
from Topic_Modeling import Topic_Sentiment_modeling
from Topic_Modeling_PO import Topic_Sentiment_modeling_PO
from modelc_integration import prediction_mode
from userInstagram import instagramapi
from PIL import Image
from glob import glob
import pandas as pd
PEOPLE_IMAGES = os.path.join('static/web/', 'profile')
hash_tag = os.path.join('static/', 'web')
import json
from datetime import datetime
import pickle
# Route for handling the login page logic
# import the Flask class from the flask module
import time

# create the application object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_IMAGES
app.config['DOWNLOAD_FOLDER'] = hash_tag
app.config['MODEL_FOLDER'] = os.path.join(os.getcwd(), 'pythonlib')

path_hash = os.path.join(app.config['DOWNLOAD_FOLDER'],'hashtag')
path_tag_accounts = os.path.join(app.config['DOWNLOAD_FOLDER'],'tag_accounts')

app.secret_key = 'super secret key'
# use decorators to link the function to a url
@app.route('/')
def home():
    flash('Login successful')
    return redirect(url_for('login'))  # return a string


@app.route('/Refresh')
def Refresh():

    with open('instagram_page.txt') as f:
        lines = f.readlines()
        
    instagram_page = lines[0]
    instagram_page = instagram_page.replace('"', '')
    instagram_page = instagram_page.replace("'", '')
    instagram = instagramapi(instagram_page)
    instagram.instaprofile()
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    best_photo_list=[]
    
    with open('instagram_page.txt') as f:
        lines = f.readlines()
        
    instagram_page = lines[0]
    instagram_page = instagram_page.replace('"', '')
    instagram_page = instagram_page.replace("'", '')
    
    path = os.path.join(app.config['UPLOAD_FOLDER'],instagram_page)
    isExist = os.path.exists(path)
    if not isExist:
        instagram = instagramapi(instagram_page)
        instagram.instaprofile()
        
    
    df_profile= pd.read_csv(path+"/"+os.path.basename(glob(path+"/PRO_*.csv")[0]))
    df_post= pd.read_csv(path+"/"+os.path.basename(glob(path+"/PO_*.csv")[0]))
    
    '''
    df_profile['PRO_description'] = df_profile.PRO_description.fillna(df_profile['PRO_full_name'])
    PRO_Topic_modelling  = Topic_Sentiment_modeling(df_profile['PRO_description'],instagram_page,'pro')
    PRO_Topic_modelling.description_processing()
    time.sleep(3)
    
    PO_Topic_modelling  = Topic_Sentiment_modeling_PO(df_post['PO_description'],instagram_page,'po')      
    print(PO_Topic_modelling)
    PO_Topic_modelling.description_processing()        
        
    time.sleep(3)    
    
    prediction_mode_com = prediction_mode(df_profile,df_post,instagram_page)
    prediction_mode_com.datamerge()
    time.sleep(3)
    
    PO_Topic_modelling  = Topic_Sentiment_modeling(df_post['PO_description'],instagram_page,'po')        
    PO_Topic_modelling.description_processing()
    
    PRO_Topic_modelling  = Topic_Sentiment_modeling(df_profile['PRO_description'],instagram_page,'pro')
    PRO_Topic_modelling.description_processing()
    '''
        
    df_topic_po= pd.read_csv(path+"/"+os.path.basename(glob(path+"/TM_po_*.csv")[0]))
    df_topic_pro= pd.read_csv(path+"/"+os.path.basename(glob(path+"/TM_pro_*.csv")[0]))
    
    df_profile = pd.merge(df_profile, df_topic_pro, left_index=True, right_index=True)
    df_post = pd.merge(df_post, df_topic_po, left_index=True, right_index=True)
    
    prediction_mode_com = prediction_mode(df_profile,df_post,instagram_page)  
    prediction_mode_com.datamerge()
       
    #df_profile.columns = 'PRO_' + df_profile.columns
    #df_post.columns = 'PO_' + df_post.columns
    
    df_model_c = pd.read_csv(path+"/"+os.path.basename(glob(path+"/Model_c_*.csv")[0]))
    
    Actual_Like = list(df_post['PO_PO_numbr_likes'].head(20))
    Actual_Comment = list(df_post['PO_PO_number_comments'].head(20))
    Predicted_Like = list(df_model_c['y_likes_pred'].head(20))
    Predicted_Comment = list(df_model_c['y_comments_pred'].head(20))
    df_post["Period"] = df_post["PO_Year"].map(str) + "-" + df_post['PO_Month'].apply(lambda x: calendar.month_abbr[x])
    df_model_c["Period"] = df_model_c["Year"].map(str) + "-" + df_model_c['Month'].apply(lambda x: calendar.month_abbr[x])

    topic_label=[]
    #topic_label_list=[]
    files = glob(path+"/Topic_*.csv", recursive = True)
    for file in files:
       topic_label_csv = pd.read_csv(file)
       for col in topic_label_csv.columns:
           if not col.startswith('Unnamed'): 
              topic_label.append(col)
    
       
    
    #rating=[]
    #topic_label_list=[]
    files = glob(path+"/rating*.csv", recursive = True)
    for file in files:
       rating_csv = pd.read_csv(file,header = None)
       rating = rating_csv.values.tolist()
       
       
    #topic_label = topic_label[:-1]
    #topic_label_list = list(topic_label)
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
    df_profile['PRO_dominant_topic'] = df_profile["PRO_dominant_topic"].map(dominant_topic_names)
    df_post['PO_dominant_topic_names'] = df_post["PO_dominant_topic"].map(dominant_topic_names)
    
    if df_profile['PRO_PRO_is_business'][0] ==False:
       df_profile['PRO_PRO_is_business'] = 'Ouch. You will need to turn on Instagram Business Account.'
    else:
       df_profile['PRO_PRO_is_business'] = 'You are using instagram business account.'''
    
    df_profile["PRO_compound_name"] = np.where(df_profile["PRO_compound"] > 0.0, 'Positive',df_profile["PRO_compound"])
    df_profile["PRO_compound_name"] = np.where(df_profile["PRO_compound"] < 0.0, 'Negative',df_profile["PRO_compound"])
    df_profile["PRO_compound_name"] = np.where(df_profile["PRO_compound"] == 0.0, 'Neutral',df_profile["PRO_compound"])
    df_profile['total_likes'] = df_post['PO_PO_numbr_likes'].sum()     
    df_profile['median_likes'] = df_post['PO_PO_numbr_likes'].median() 
    df_profile['median_comments'] = df_post['PO_PO_number_comments'].median() 
    df_profile['pred_median_likes'] = df_model_c['y_likes_pred'].median() 
    df_profile['pred_median_comments'] = df_model_c['y_comments_pred'].median() 
    df_profile['total_comments'] = df_post['PO_PO_number_comments'].sum()    
    df_profile['Percentage_Achieved_likes'] = df_profile['total_likes']*100/df_model_c['y_likes_pred'].sum()     
    df_profile['Percentage_Achieved_comment'] = df_profile['total_comments']*100/df_model_c['y_comments_pred'].sum()   
    df_profile['Percentage_Viewership_likes'] = df_post.loc[df_post['PO_PO_post_type'] == 2, 'PO_PO_numbr_likes'].sum()  *100 / df_post['PO_PO_number_view_count'].sum()
    
    df_profile['Percentage_Achieved_likes'] = df_profile['Percentage_Achieved_likes'].round(0)
    df_profile['Percentage_Achieved_comment'] = df_profile['Percentage_Achieved_comment'].round(0)
    df_profile['Percentage_Viewership_likes']  = df_profile['Percentage_Viewership_likes'].round(0)
    post_type_list = []
    post_type_actual = df_post.groupby(['PO_PO_post_type'])['PO_PO_numbr_likes'].agg('sum').reset_index()
    

    iposttype = [1,2,8]
    for i in iposttype:    
        if i not in list(post_type_actual['PO_PO_post_type']):
            new_row = {'PO_PO_post_type':i, 'PO_PO_numbr_likes':1}
            post_type_actual = post_type_actual.append(new_row, ignore_index=True)
            
    post_type_actual['PO_PO_numbr_likes'] = post_type_actual['PO_PO_numbr_likes'].replace(0, 1)
    post_type_actual = post_type_actual.sort_values(by=['PO_PO_post_type'])
    print(post_type_actual)
    post_type_predicted = df_model_c.groupby(['PO_post_type'])['y_likes_pred'].agg('sum').reset_index()
    
    for j in iposttype: 
        print('test')
        if j not in list(post_type_predicted['PO_post_type']) :
            print(j)
            new_row = {'PO_post_type':j, 'y_likes_pred':1}
            post_type_predicted = post_type_predicted.append(new_row, ignore_index=True)
    post_type_predicted = post_type_predicted.sort_values(by=['PO_post_type'])
    
    post_type_predicted = post_type_predicted.replace(0, 1)
    print(post_type_predicted)
    
    post_type_actual = pd.merge(post_type_actual, post_type_predicted, left_index=True, right_index=True)

    
    for column in post_type_actual.columns:
        list1 = post_type_actual[column].tolist()
        post_type_list.append(list1)
    
    
    print("post_type_numbers", post_type_list[0][0],post_type_list[1][0])
    df_profile['Percentage_Achieved_photos'] = post_type_list[0][0] * 100 / post_type_list[1][0]
    df_profile['Percentage_Achieved_videos'] = post_type_list[0][1] * 100 / post_type_list[1][1]
    df_profile['Percentage_Achieved_albums'] =  post_type_list[0][2] * 100 / post_type_list[1][2]
    
    df_profile['Percentage_Achieved_photos'] = df_profile['Percentage_Achieved_photos'].round(0)
    df_profile['Percentage_Achieved_videos'] = df_profile['Percentage_Achieved_videos'].round(0)
    df_profile['Percentage_Achieved_albums'] = df_profile['Percentage_Achieved_albums'].round(0)
    
    post_count_period = df_post.groupby(['PO_Year','PO_Month','Period'])['PO_PO_numbr_likes'].agg('count').reset_index()
   
    df_profile['post_count_period_median'] = post_count_period['PO_PO_numbr_likes'].median() 
    df_profile['post_count_period_median'] = df_profile['post_count_period_median'].round(0)
    
    target_posts = df_profile['post_count_period_median'][0] * 45/31 
    now = datetime.now()
    yearmn = now.strftime("%Y-%b")
    current_post_count = list(post_count_period.loc[(post_count_period['Period']==yearmn)]['PO_PO_numbr_likes'])
    
    if bool(current_post_count) == False:
        current_post_count = [0]
        
    df_profile['current_post_count']=int(current_post_count[0])
    df_profile['current_post_count'] = df_profile['current_post_count'].round(0)
    
    
    if target_posts <= 20:
        df_profile['post_count_period_median_target'] = 20
        df_profile['per_post_count_period'] = df_profile['current_post_count']*100/20        
        df_profile['per_post_count_period'] = df_profile['per_post_count_period'].round(0)
    
    elif target_posts >= 21 or target_posts <= 75:
        df_profile['post_count_period_median_target'] = target_posts
        df_profile['post_count_period_median_target'] = df_profile['post_count_period_median_target'].round(0)
        df_profile['per_post_count_period'] = df_profile['current_post_count']*100/target_posts
        df_profile['per_post_count_period'] = df_profile['per_post_count_period'].round(0)
        
    else:
        df_profile['post_count_period_median_target'] = 'You have reached the most number of posts per day. Enjoy following the same.'
        df_profile['per_post_count_period'] = current_post_count[0]*100/target_posts
        df_profile['per_post_count_period'] = df_profile['per_post_count_period'].round(0)
    
    df_profile['impressions'] = ((df_post['PO_PO_numbr_likes']+df_post['PO_PO_number_comments'])*100/df_profile["PRO_PRO_follower_count"]).agg('median') 
    

    
    
    profile_name_list = df_profile.iloc[0].to_list()
    
    post_type_actual = df_post.groupby(['PO_PO_post_type', 'PO_PO_numbr_likes'])['PO_PO_numbr_likes'].agg('sum')
    profile_photo_name = os.path.basename(glob(path+'/img/PRO_*.jpg')[0])
    profile_photo_main = os.path.join(app.config['UPLOAD_FOLDER'],instagram_page+"/img/"+profile_photo_name)
    
    
    
    li=[]
    res = {}
    hashtag = list(df_post.PO_hashtag)

    hashtag = [item for item in hashtag if not(pd.isnull(item)) == True]
    if not hashtag:
        hashtag = [instagram_page]
        
    split_list = list([x.split() for x in hashtag])
    #print(split_list)
    for i in split_list:
       li = li + i
       
    for i in li:
        res[i] = li.count(i)
    
    
    hashtags = pd.DataFrame(res.items())
    
    hashtags = hashtags.sort_values(by=[1], ascending=False)
    hashtags = hashtags.reset_index(drop=True)
    hashtag = list(hashtags[hashtags.columns[0]].head(5))
    '''#hashtags.set_index(hashtags.columns[0], inplace = True)
    hashtags = hashtags.head(50)
    dc_hashtag = hashtags.set_index(hashtags.columns[0])[hashtags.columns[1]].to_dict()
    data = {'Hashtags' : 'count'}
    data.update(dc_hashtag)'''
 
    for file in sorted(glob(path+'/img/PO_*.jpg'), key=os.path.getmtime):
        best_photo_test = os.path.join(app.config['UPLOAD_FOLDER'],instagram_page+"/img/"+os.path.basename(file))
        best_photo_list.append(best_photo_test) 
            

    post_type_actual = df_post.groupby(['PO_Year','PO_Month','Period'])['PO_PO_numbr_likes'].agg('sum')

    post_type_predicted = df_model_c.groupby(['Year','Month','Period'])['y_likes_pred'].agg('sum')

    post_type_actual = pd.merge(post_type_actual,post_type_predicted, left_index=True, right_index=True)

    post_type_actual = post_type_actual.reset_index()

    title = "Actual vs Predicted likes"
    temps = post_type_actual[['Period','PO_PO_numbr_likes','y_likes_pred']]
    #temps['Period'] = temps['Period'].astype(str)
    
    d = temps.values.tolist()
    c = temps.columns.tolist()
    d.insert(0,c)
    tempdata = json.dumps({'title':title,'data':d})
    '''
    title_topic = "Topics Vs Likes (Median)"
    topic =  df_post.groupby('dominant_topic_names').agg({'dominant_topic':'count', 'PO_numbr_likes': 'median'}).reset_index().rename(columns={'dominant_topic':'Dominant Topic Count','PO_numbr_likes':'Likes (median)'})
    topic['dominant_topic_names'] = topic['dominant_topic_names'].astype(str)
    
    b = topic.values.tolist()
    a = topic.columns.tolist()
    b.insert(0,a)
    topic_data = json.dumps({'title':title_topic,'data':b})'''
    
    

   
    title_topic = "Topics and Performance"
    topic =  df_post.groupby('PO_dominant_topic_names').agg({'PO_dominant_topic':'count', 'PO_PO_numbr_likes': 'median'}).reset_index().rename(columns={'PO_dominant_topic':'Dominant Topic Count','PO_PO_numbr_likes':'Likes (median)'})
    topic['PO_dominant_topic_names'] = topic['PO_dominant_topic_names'].astype(str)
    
    
    
    topic['Topic Performance (%)'] = topic['Likes (median)'] * 100 / (topic['Dominant Topic Count'])
    topic = topic.sort_values(by=['Topic Performance (%)'], ascending=False)
    #topic = topic[topic['dominant_topic_names','Dominant Topic Count','Topic Performance (%)']]
    
    top_topic_list = list(topic['PO_dominant_topic_names'].head(3))
    top_topic_list.append(df_post['PO_PO_description'][0])
    f = topic.values.tolist()
    e = topic.columns.tolist()
    f.insert(0,e)
    topic_data = json.dumps({'title':title_topic,'data':f})
    
    topic = topic[['PO_dominant_topic_names','Topic Performance (%)']]
    
    dc_hashtag = topic.set_index(topic.columns[0])[topic.columns[1]].to_dict()
    data = {'Dominant Topic Names' : 'Topic Performance (%)'}
    data.update(dc_hashtag)
    
    df_hashtag_recommend_list = []
    top_topic_list_name = [top_topic_list[0],top_topic_list[1],top_topic_list[2]]
    for topics_list_file in top_topic_list_name:
        df_hashtag_recommend= pd.read_csv(path_hash+'/'+topics_list_file+'_Hashtag.csv')
        df_hashtag_recommend=df_hashtag_recommend[df_hashtag_recommend['Impressions'].between(df_profile['impressions'][0],df_profile['impressions'][0]+2)]
        df_hashtag_recommend = df_hashtag_recommend.sort_values(by=['Impressions'], ascending=False)
        df_hashtag_recommend = df_hashtag_recommend.head(3)
        
        hash_row_count = df_hashtag_recommend.shape[0]
        if hash_row_count ==0:
            df_hashtag_recommend_list = list(hashtags[hashtags.columns[0]].head(10))
        
        else: 
            for column in df_hashtag_recommend.PO_hashtags:
                df_hashtag_recommend_list.append(column)
        
    df_tagaccounts_recommend_list=[]
    for topics_list_file in top_topic_list_name:
        df_tagaccounts_recommend= pd.read_csv(path_tag_accounts+'/'+topics_list_file+'_tag_accounts.csv') 
        df_tagaccounts_recommend= df_tagaccounts_recommend[df_tagaccounts_recommend['Impressions'].between(df_profile['impressions'][0],df_profile['impressions'][0]+100)]
        df_tagaccounts_recommend = df_tagaccounts_recommend.sort_values(by=['Impressions'], ascending=False)
        df_tagaccounts_recommend = df_tagaccounts_recommend.head(3)
        
        hash_row_count = df_tagaccounts_recommend.shape[0]
        if hash_row_count ==0:                
            
            li=[]
            res = {}
            tag_accounts = list(df_post.PO_tag_accounts)
            tag_accounts = [item for item in tag_accounts if not(pd.isnull(item)) == True]
            if not tag_accounts:
                tag_accounts = [instagram_page]
            split_list = list([x.split() for x in tag_accounts])
            
            for i in split_list:
               li = li + i
               
            for i in li:
                res[i] = li.count(i)
                
            tag_accounts_df = pd.DataFrame(res.items())
            tag_accounts_df = tag_accounts_df.sort_values(by=[1], ascending=False)
            tag_accounts_df = tag_accounts_df.reset_index(drop=True)
            df_tagaccounts_recommend_list = list(tag_accounts_df[tag_accounts_df.columns[0]].head(10))
        
        else: 
            for column in df_tagaccounts_recommend.PO_tag_accounts:
                df_tagaccounts_recommend_list.append(column)
                
        #df_tagaccounts_recommend_list.append(path_tag_accounts+'/'+topics_list_file+'_tag_accounts.csv')
    
    
    '''
    
    #profile_photo_main = 'Archie Photo'  '''
    return render_template('welcome.html',profile_name =profile_name_list,profile_photo=profile_photo_main,best_photo=best_photo_list,topic_label=topic_label,hashtag=hashtag,data=data,    Actual_Like = Actual_Like,Actual_Comment=Actual_Comment,Predicted_Like = Predicted_Like,Predicted_Comment=Predicted_Comment,tempdata=tempdata,title=title,topic_data=topic_data,title_topic=title_topic,top_topic_list=top_topic_list,df_hashtag_recommend_list=df_hashtag_recommend_list,df_tagaccounts_recommend_list=df_tagaccounts_recommend_list,rating=rating)  # render a template

# start the server with the 'run()' method
if __name__ == '__main__':
    #app.config['DEBUG'] = True
    app.run(debug=True)
    #app.run()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    global instagram_page
    if request.method == 'POST':
        person1 = userauthentication(request.form['username'], request.form['password'],'')  
        login_message = person1.LoginCheck()
        #print(login_message[0])
        if login_message[0] == 'Successful Login':
            flash('Login successful')
            instagram_page =  login_message[1]
            #BASE_DIR  = os.getcwd()
            BASE_DIR = ''.join(os.path.dirname(os.getcwd()))
            path = BASE_DIR+"/static/web/profile/"+instagram_page
            isExist = os.path.exists(path)
            #instagram_page.to_csv(self.path+"/TM_"+self.po_pro_type+"_"+self.profile+".csv",index=False)
            file = open("instagram_page.txt", "w")
            instagram_page_value = repr(instagram_page)
            file.write(instagram_page_value)
            file.close
            #if not isExist:
            #    instagram = instagramapi(instagram_page)
            #    instagram.instaprofile()
   
            #profile_photo = Image.open(path+"/img/"+os.path.basename(glob.glob(path+'/img/PRO_*')[0]))
            
            #df_profile= 'Archie + Pluto'#pd.read_csv(path+"/"+os.path.basename(glob.glob(path+"/PRO_*.csv")[0]))
            #df_profile['PRO_full_name'] 
            return redirect(url_for('welcome'))
            #return redirect(url_for('welcome'))
            #flash('Invalid Credentials. Please try again.',category)
            error = login_message
            #error = 'Invalid Credentials. Please try again.'
        else:
            error = login_message[0]
            
    return render_template('login.html', error=error)


@app.route('/Change_Password', methods=['GET', 'POST'])
def ChangePassword():
    error = None
    if request.method == 'POST':
        # do stuff when the form is submitted
        if request.form['password'] == request.form['Retypepassword']:
            person1 = userauthentication(request.form['username'], request.form['password'],'')  
            ChangePassword_message = person1.py_changepassword()
            return redirect(url_for('welcome'))
        elif request.form['password'] != request.form['Retypepassword']: 
            error = 'Password does not match'
            
        else:
            error = 'Password is not changed. please try again later.'
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        

    # show the form, it wasn't submitted
    return render_template('Change_Password.html', error=error)
    
@app.route('/Register_Form', methods=['GET', 'POST'])    
def Registration():
    error = None
    if request.method == 'POST':
        
        person1 = userauthentication(request.form['username'], request.form['password'],request.form['Instagram_Account'])  
        ChangePassword_message = person1.registration()
        
        if ChangePassword_message[0]=='User already exists. Please use login screen to login.':
            error=ChangePassword_message[0]
        else:
            #error=ChangePassword_message[0]
            return redirect(url_for('login'))
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        
    # show the form, it wasn't submitted
    return render_template('Register_Form.html', error=error)