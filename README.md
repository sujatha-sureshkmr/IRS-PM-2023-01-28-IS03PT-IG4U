 

Summary:
This guide provides steps for installation and usage of the app. Mac operating system is used for the preparation of the guide. Other operating system uses the same steps unless otherwise stated.


Pre-requisites
Operating System
1.	Linux
2.	Windows
3.	Mac
Required Programs
1.	Anaconda (we have tested our application based on conda installation of python. Any standalone installation or other type of installation may require self troubleshooting if found any errors)
2.	Python

Install python libraries
1.	Please use admin account for this application before installation and usage of the application. 
Example: For windows, run the terminal as administrator
For linux and mac: use sudo su 

2.	Please run following steps in the terminal
pip install psycopg2
pip install nltk
python 
import nltk
nltk.download('stopwords')
conda update --force conda
conda install -c conda-forge scikit-surprise

3.	Please install following libraries
pip install  beautifulsoup4==4.11.1
pip install  ChatterBot==1.0.2
pip install  chatterbot-corpus==1.2.0
pip install  confection==0.0.4
pip install  constantly==15.1.0
pip install  contourpy==1.0.5
pip install  cookiecutter==1.7.3
pip install  cryptography==38.0.4
pip install  cssselect==1.1.0
pip install  cycler==0.11.0
pip install  cymem==2.0.7
pip install  Cython==0.29.32
pip install  cytoolz==0.12.0
pip install  daal4py==2021.6.0
pip install  dask==2022.7.0
pip install  datashader==0.14.3
pip install  datashape==0.5.4
pip install  debugpy==1.5.1
pip install  decorator==5.1.1
pip install  defusedxml==0.7.1
pip install  demoji==1.1.0
pip install  dictdiffer==0.9.0
pip install  diff-match-patch==20200713
pip install  distributed==2022.7.0
pip install  Flask==1.1.2
pip install  gensim==4.1.2
pip install  glob2==0.7
pip install  gmpy2==2.1.2
pip install  instagrapi==1.17.6
pip install  Jinja2==2.11.3
pip install  jinja2-time==0.2.0
pip install  langcodes==3.3.0
pip install  langdetect==1.0.9
pip install  lazy-object-proxy==1.6.0
pip install  matplotlib==3.6.2
pip install  matplotlib-inline==0.1.6
pip install  neo4j==5.5.0
pip install  numpy==1.21.5
pip install  pandas==1.4.4
pip install  pandocfilters==1.5.0
pip install  panel==0.14.2
pip install  param==1.12.3
pip install  parsel==1.6.0
pip install  parso==0.8.3
pip install  partd==1.2.0
pip install  pathlib==1.0.1
pip install  pathspec==0.9.0
pip install  pathy==0.10.1
pip install  patsy==0.5.3
pip install  pep8==1.7.1
pip install  requests==2.28.1
pip install  requests-file==1.5.1
pip install  s3transfer==0.6.0
pip install  scikit-image==0.19.3
pip install  scikit-learn==1.0.2
pip install  scikit-surprise==1.1.3
pip install  scipy==1.10.0
pip install  Scrapy==2.6.2
pip install  seaborn==0.12.2
pip install  spacy==3.5.0
pip install  spacy-legacy==3.0.12
pip install  spacy-loggers==1.0.4
pip install  SQLAlchemy==1.2.19
pip install  wheel==0.40.0
pip install  widgetsnbextension==3.5.2
pip install translate
pip install demoji

IG4U App
Download App
GIthub Link: 

Download the source from the above mentioned github link. Unzip the file “Instawebsite.zip”.

Start App IG4U 
1.	From Finder(Mac), Files(Linux), File Explorer (Windows): Go into the unzipped folder. Folder contents looks below
 
2.	Right click and choose “Open in Terminal”

 

3.	Please use admin account for this application before installation and usage of the application. 
Example: For windows, run the terminal as administrator
For linux and mac: use sudo su 
4.	For Mac/Linux systems run the following commands:
export FLASK_APP=app
export FLASK_DEBUG=1
flask run

5.	For Windows run the following commands:
set FLASK_APP=app
set FLASK_DEBUG=1
flask run

6.	Identify the URL that is set by flask: 
By default: http://127.0.0.1:5000/
 
7.	Go to any web browser (Chrome/Safari/Firefox) and paste/type the URL given in flask. E.g. http://127.0.0.1:5000/
Eureka!! Now you can access the IG4U app. 

Here is the test account for IG4U login.

Field Name	Value
Username	test
Password	123456789



 

8.	As a first time user, you will need to register. Click Register here. Update information and click Register. You will be directed to login page. Please use your credentials to login.

Field Name	Value
Username	Username that you will use to login to IG4U Password
Password	Password 
Instagram Account Name	Input Instagram account name that you would like to analyse.
Incase, you do not have any Instagram account. You may use our test account:  
Archieplutowaggingtails



 

9.	Forget Password – Forget password page helps to reset your password in case you forget. From login page -> Click Forget Password.
Field Name	Value
Username	Username that you will use to login to IG4U Password
Password	Password 
Re-type Password	Password 


 

10.	Once successful login, you will be directed to the home page.

 

Here are the details of the main page:
Field Name	Description
Background Image	Displays the photo that received the most impression among all posts from your profile.
1	Instagram Page Profile Photo
2	Instagram Page Full Name as registered
3	Instagram profile has went through data processing and topic modelling. “I am Known for” is what defines the Instagram page.
4	You can also directly visit your Instagram page by clicking Instagram icon.
5	Home Page -> will direct you to this screen when you click.
6	Refresh -> Allows you to refresh the datasets and generating new info from the Instagram. By default, system will fetch the previously generated information that is saved in your local machine.
7	About -> brings to about page
8	Fact -> bring to fact page.
9	Performace -> bring to performance page
10	Prediction -> bring to Prediction
11	Recommendation -> bring to Recommendation
12	Portfolio -> bring to Portfolio
13	Logout  -> logout from IG4U account

11.	About
  

Field Name	Description
1	Instagram profile has went through data processing and topic modelling. “I am Known for” is what defines the Instagram page.
2	Displays the photo that received the second most impression among all posts from your profile.
3	Instagram Category -> Instagram profile went through topic modelling with respect to the training dataset of 3 Million records and identifies which topic this page belongs too. For example: what is the category of the Instagram page.
4	Profile Sentiment -> Instagram profile gone through sentiment analysis and identifies the overall sentiment of the profile
5	Received Likes (Median) : Median Likes for the over all posts that the page received.
6	Predicted Likes (Median): Instagram profiles went through prediction modelling and captures what is the likes that this Instagram page is capable of getting for example: This profile has a potential to receive 217 likes in median.
7	Received Comments (Median) : Median Comments for the over all posts that the page received.
8	Predicted Comments (Median): Instagram profiles went through prediction modelling and captures what is the Comments that this Instagram page is capable of getting for example: This profile has a potential to receive 217 Comments in median.
9	Most Frequent Hashtag: the hashtags that the page had used. 
10	Business Account : displays if this Instagram account is business account or not.
Business Account is free. It provides lots of benefits for the reach and impression of the posts. 

12.	Fact
 

Field Name	Description
1	Media Count -> number of posts by the Instagram page
2	Follower Count -> Total number of followers for this Instagram page
3	Following Count -> How many accounts that the page is following
4	Impressions -> Impression of the page
Impression = (total number of likes + comments on Instagram) * 100 / follower count
5	Topics and Performance:
Instagram page posts went through topic modelling and identifies each post to 10 identified topics.  Analysis its impressions for each topic and captures top performing topics.
Note:
Topics are categorised into : PO_Food, PO_Work_Event, PO_Lifestyle_Health, PO_Fitness, PO_Travel_Celebrations, PO_Hobby, PO_Beauty_Makeup, PO_Skincare_Treatment, PO_Life_Happiness, PO_Shop_Business_Advertisement


13.	Performance
 

Field Name	Description
1	Percentage Received Likes -> Target is assumed to be predicted number of likes with respect to 3 Million training records (Prediction Modelling).
2	Percentage Received Comments -> Target is assumed to be predicted number of Comments with respect to 3 Million training records (Prediction Modelling).
3	Percentage Viewership Likes -> Target is assumed to be predicted number of likes based on viewership with respect to 3 Million training records (Prediction Modelling).
4	Percentage Likes Achieved Photos -> Target is assumed to be predicted number of likes by post type photos with respect to 3 Million training records (Prediction Modelling).
5	Percentage Likes Achieved Videos  -> Target is assumed to be predicted number of likes by post type videos with respect to 3 Million training records (Prediction Modelling).
6	Percentage Likes Achieved Albums -> Target is assumed to be predicted number of likes by post type albums with respect to 3 Million training records (Prediction Modelling).

14.	Prediction
 


Field Name	Description
1	Shows the line graph for the total number of likes vs predicted likes based on each posts with the time-frame.
2	Instagram page posts went through topic modelling and identifies each post to 10 identified topics.  Analysis its impressions for each topic and captures top performing topics.
Note:
Topics are categorised into : PO_Food, PO_Work_Event, PO_Lifestyle_Health, PO_Fitness, PO_Travel_Celebrations, PO_Hobby, PO_Beauty_Makeup, PO_Skincare_Treatment, PO_Life_Happiness, PO_Shop_Business_Advertisement


15.	Recommendation
 

Field Name	Description
1	Consistency : How many posts that the profile user needs to post for traction. 
2	Hashtags: Identify famous hashtags that belongs to top 3 topic performance for the page through content based association ruling. Rating for the hashtags retrieved through ranking modelling.  
3	Identify top performing topics based on impressions and recommend those topics. 
4	Account Tagging: Identify famous accounts to tag that belongs to top 3 topic performance for the page through content based association ruling. Rating for the hashtags retrieved through ranking modelling 
5	Suggestion on creating an engaging advertisement through instragram. 



16.	Portfolio
 


Field Name	Description
1	Displays top 9 photos that the Instagram profile received based on the impression
2	Shows Actual Likes and Predicted likes for the posts based on predicted number of likes with respect to 3 Million training records (Prediction Modelling).

![image](https://github.com/sujatha-sureshkmr/IRS-PM-2023-01-28-IS03PT-IG4U/assets/44421667/e9eaae00-35cc-4c3d-b794-09235a99e00b)
