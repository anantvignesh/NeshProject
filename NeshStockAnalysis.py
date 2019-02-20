"""
Created on Sat Feb 16 09:21:57 2019

@author: Anant Vignesh
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from google.colab import drive

#------------------Mounting Drive------------------#

drive.mount('/content/drive')
!ls -l "/content/drive/My Drive/DataSet/HeartDiseasePrediction"

#------------------Data Scrapping------------------#

from urllib.request import urlopen
from bs4 import BeautifulSoup

company_list = ["OXY", "EOG", "APC", "APA", "COP", "PXD"]

#Collecting Stock Data
stock_url_list = ["https://www.nasdaq.com/symbol/oxy/historical", "https://www.nasdaq.com/symbol/eog/historical", "https://www.nasdaq.com/symbol/apc/historical",
                  "https://www.nasdaq.com/symbol/apa/historical", "https://www.nasdaq.com/symbol/cop/historical", "https://www.nasdaq.com/symbol/pxd/historical"
                 ]
for url,company_name in zip(stock_url_list,company_list):
  html = urlopen(url)
  soup = BeautifulSoup(html, 'lxml')
  table_tag = soup.find_all('td')
  content = []
  stockdata = []
  for tag_str in table_tag:
    cleantext = BeautifulSoup(str(tag_str),"lxml").get_text()
    content.append(cleantext.strip())
  content = content[9:]
  
  for i in range(0,(len(content)+1),6):
    stockdata.append(content[i:i+6])
  stock_dataset = pd.DataFrame(stockdata[:64], columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
  stock_dataset.head()
  file_name = '/content/drive/My Drive/DataSet/'+company_name+'_StockData.csv'
  stock_dataset.to_csv(file_name, index = False)
  
#Collecting Latest News Articles
url_list = ["https://www.fool.com/quote/nyse/occidental-petroleum/oxy","https://www.fool.com/quote/nyse/eog-resources/eog",
            "https://www.fool.com/quote/nyse/anadarko-petroleum/apc","https://www.fool.com/quote/nyse/apache/apa",
            "https://www.fool.com/quote/nyse/conocophillips/cop","https://www.fool.com/quote/nyse/pioneer-natural-resources/pxd"]
temp = []
for url, name in zip(url_list, company_list):
  latest_news = []
  html = urlopen(url)
  soup = BeautifulSoup(html, 'lxml')
  article_tag = soup.find_all('a', attrs={'class': 'article-link'})
  for i in range(0,5):
    content = ""
    html2 = urlopen(article_tag[i].get('href'))
    soup2 = BeautifulSoup(html2, 'lxml')
    content_tag = soup2.find('span', attrs = {'class' : 'article-content'})
    for tag in content_tag:
      tag = (BeautifulSoup(str(tag),"lxml").get_text()).strip()
      content = content + tag
df_article = pd.DataFrame(latest_news, columns = ['Company','Article Title','Article Link'])
df_article.to_csv('/content/drive/My Drive/DataSet/ArticleList.csv', index = False)

#Collecting Net Flow Cash Data
netcashflow_url_list = ["https://finance.yahoo.com/quote/OXY/cash-flow/", "https://finance.yahoo.com/quote/EOG/cash-flow/",
                        "https://finance.yahoo.com/quote/APC/cash-flow/", "https://finance.yahoo.com/quote/APA/cash-flow/",
                        "https://finance.yahoo.com/quote/COP/cash-flow/", "https://finance.yahoo.com/quote/PXD/cash-flow/"]
for url,company_name in zip(netcashflow_url_list,company_list):
  netcashflow_content = []
  netcashflow_data = []
  ncf_data_final = []
  html = urlopen(url)
  soup = BeautifulSoup(html, 'lxml')
  table_tag = soup.find_all('td', attrs = {'class' : ['Fw(600)', 'Fz(s)', 'Ta(end)', 'Pb(20px)']})
  for tag in table_tag:
    cleantext = BeautifulSoup(str(tag),"lxml").get_text()
    netcashflow_content.append(((cleantext.strip()).replace("/","-")).replace(",", ""))
  netcashflow_content = netcashflow_content[4:]
  for i in range(0,(len(netcashflow_content)+1),5):
    netcashflow_data.append(netcashflow_content[i:i+5])
  netcashflow_data[7][0] = 'NCF OprAct'
  netcashflow_data[11][0] = 'NCF InvAct'
  netcashflow_data[16][0] = 'NCF FinAct'
  
  ncf_data_final.append(netcashflow_data[7])
  ncf_data_final.append(netcashflow_data[11])
  ncf_data_final.append(netcashflow_data[16])
  netcashflow_dataset = pd.DataFrame(ncf_data_final, columns = ['Category', '2018', '2017', '2016', '2015'])
  file_name = '/content/drive/My Drive/DataSet/Nesh/NetCashFlow_Data/'+company_name+'_NetCashFlowData.csv'
  netcashflow_dataset.to_csv(file_name, index = False)
  
#Collecting Total Revenue Data
revenue_url_list = ["https://finance.yahoo.com/quote/OXY/financials/", "https://finance.yahoo.com/quote/EOG/financials/", 
                    "https://finance.yahoo.com/quote/APC/financials/", "https://finance.yahoo.com/quote/APA/financials/", 
                    "https://finance.yahoo.com/quote/COP/financials/", "https://finance.yahoo.com/quote/PXD/financials/"]

revenue_content = []
for url,name in zip(revenue_url_list,company_list):
  tempcontent = []
  html = urlopen(url)
  soup = BeautifulSoup(html, 'lxml')
  revenuedata = soup.find_all('td', attrs = {'class' : ['Fz(s)','Ta(end)','Pstart(10px)']})
  for val in revenuedata:
    cleantext = BeautifulSoup(str(val),"lxml").get_text()
    tempcontent.append((((cleantext.strip()).replace("\n\n"," ")).replace("\n", " ")).replace(',',''))
  tempcontent = tempcontent[4:9]
  tempcontent[0] = name
  revenue_content.append(tempcontent)
revenue_dataset = pd.DataFrame(revenue_content, columns = ['Company Name', '2018', '2017', '2016', '2015'])
file_name = '/content/drive/My Drive/DataSet/Nesh/RevenueData.csv'
revenue_dataset.to_csv(file_name, index = False)

#Collecting Call Transcript Data
call_url = ["https://www.nasdaq.com/aspx/call-transcript.aspx?StoryId=4240792&Title=occidental-petroleum-corporation-oxy-ceo-vicki-hollub-on-q4-2018-results-earnings-call-transcript",
            "https://www.nasdaq.com/aspx/call-transcript.aspx?StoryId=4217614&Title=eog-resources-eog-q3-2018-results-earnings-call-transcript",
            "https://www.nasdaq.com/aspx/call-transcript.aspx?StoryId=4238690&Title=anadarko-petroleum-corporation-apc-ceo-al-walker-on-q4-2018-results-earnings-call-transcript",
            "https://www.nasdaq.com/aspx/call-transcript.aspx?StoryId=4217351&Title=apache-apa-q3-2018-results-earnings-call-transcript",
            "https://www.nasdaq.com/aspx/call-transcript.aspx?StoryId=4237353&Title=conocophillips-cop-ceo-ryan-lance-on-q4-2018-results-earnings-call-transcript",
            "https://www.nasdaq.com/aspx/call-transcript.aspx?StoryId=4241233&Title=pioneer-natural-resources-company-pxd-ceo-tim-dove-on-q4-2018-results-earnings-call-transcript"]
call_data = []
for url, company_name in zip(call_url, company_list):
  member_list = []
  html = urlopen(url)
  soup = BeautifulSoup(html, 'lxml')
  member_tags = soup.findChildren('p')
  member_tags = member_tags[5:]
  for member in member_tags:
    member = (BeautifulSoup(str(member),"lxml").get_text()).strip()
    if member not in member_list and member not in ['Company Participants', 'Conference Call Participants', 'Executives', 'Analyst']:
      member_list.append(member)
  member_list = member_list[:member_list.index('Presentation')]
  call_data.append([company_name, member_list[0], '\n'.join(member_list[1:])])
call_dataset = pd.DataFrame(call_data, columns = ['Company Name', 'Call Date', 'Call Members'])
file_name = '/content/drive/My Drive/DataSet/CallTranscriptData.csv'
call_dataset.to_csv(file_name, index = False)

#------------------Data Scrapping------------------#

#----------------Data PreProcessing----------------#

#Stock Data Preprocessing
for name in company_list:
  stockdata = pd.read_csv('/content/drive/My Drive/DataSet/Nesh/Nesh_StockData/'+name+'_StockData.csv')
  stockdata = stockdata[1:]
  stockdata['date'] = pd.to_datetime(stockdata['date'])
  stockdata.to_csv('/content/drive/My Drive/DataSet/Nesh/Nesh_StockData/'+name+'_StockData.csv', index = False)

#------------------Data Analytics------------------#

#STOCK DATA ANALYSIS
for name in company_list:
  stock_data = pd.read_csv('/content/drive/My Drive/DataSet/Nesh/Nesh_StockData/'+name+'_StockData.csv')
  
  fig = plt.figure(figsize = (20,10))
  fig.suptitle(name+' STOCK ANALYSIS (NASDAQ)', fontsize = 20)

  ax1 = fig.add_subplot(231)
  ax1.set_title('Opening and Closing Value (1 month)')
  ax1.plot(stock_data['date'][:30],
           stock_data['open'][:30],
           color = 'green', label = "Open")
  ax1.plot(stock_data['date'][:30],
           stock_data['close'][:30],
           color = 'red', label = "Close")
  ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)
  
  ax2 = fig.add_subplot(232)
  ax2.set_title('High and Low Value (1 month)')
  ax2.plot(stock_data['date'][:30],
           stock_data['high'][:30],
           color = 'green', label = "High")
  ax2.plot(stock_data['date'][:30],
           stock_data['low'][:30],
           color = 'red', label = "Low")
  ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

  ax3 = fig.add_subplot(233)
  ax3.set_title('Volume (1 month)')
  ax3.plot(stock_data['date'][:30],
           stock_data['volume'][:30],
           color = 'blue')
  ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

  plt.show()
  print("\n")

#NET CASH FLOW DATA ANALYSIS
for name in company_list:
  ncf_data = pd.read_csv('/content/drive/My Drive/DataSet/Nesh/NetCashFlow_Data/'+name+'_NetCashFlowData.csv')
  fig = plt.figure(figsize = (15,10))
  fig.suptitle(name+' NET CASH FLOW ANALYSIS (NASDAQ)', fontsize = 20)
  
  ax2 = fig.add_subplot(231)
  ax2.plot(ncf_data['Category'],
           ncf_data['2016'],
           color = 'red', label = "Net Cash Flow 2016")
  ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)
  
  ax3 = fig.add_subplot(232)
  ax3.plot(ncf_data['Category'],
           ncf_data['2017'],
           color = 'blue', label = "Net Cash Flow 2017")
  ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)
  
  ax4 = fig.add_subplot(233)
  ax4.plot(ncf_data['Category'],
           ncf_data['2018'],
           color = 'black', label = "Net Cash Flow 2018")
  ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

  plt.show()
  print("\n")
  
#REVENUE DATA ANALYSIS
revenuedata = pd.read_csv('/content/drive/My Drive/DataSet/Nesh/RevenueData.csv')
fig = plt.figure(figsize = (15,10))
fig.suptitle('REVENUE ANALYSIS (Yahoo Finance)', fontsize = 20)
 
ax2 = fig.add_subplot(231)
ax2.plot(revenuedata['Company Name'],
         revenuedata['2016'],
         color = 'red', label = "Revenue 2016")
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)
  
ax3 = fig.add_subplot(232)
ax3.plot(revenuedata['Company Name'],
         revenuedata['2017'],
         color = 'blue', label = "Revenue 2017")
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

ax4 = fig.add_subplot(233)
ax4.plot(revenuedata['Company Name'],
         revenuedata['2018'],
         color = 'black', label = "Revenue 2018")
ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

plt.show()
  
#NEWS ARTICLE PUBLISHED ANALYSIS
for name in company_list:
  print("Top 5 Latest Article On "+name+"\n")
  newsdata = pd.read_csv('/content/drive/My Drive/DataSet/Nesh/NewsArticleData/'+name+'_ArticleList.csv')
  print(newsdata.head(5))
  print('\n')

#EARNINGS CALL TRANSCRIPT ANALYSIS
calldata = pd.read_csv('/content/drive/My Drive/DataSet/Nesh/CallTranscriptData.csv')
for i in range(0,6):
  print(("Company Name: %s") %(calldata.iloc[i][0]))
  print(("Call Date: %s\n") %(calldata.iloc[i][1]))
  print(("Call Participants List: %s\n") %(calldata.iloc[i][2]))
  print("------------------\n")

#Latest News Data Analysis
import nltk
import re
nltk.download('stopwords')
call_url = ["https://www.nasdaq.com/article/3-things-to-watch-when-devon-energy-reports-q4-results-cm1101542",
            "https://www.nasdaq.com/article/should-you-invest-in-the-ishares-us-oil-amp-gas-exploration-amp-production-etf-ieo-cm1099798",
            "https://www.nasdaq.com/article/noble-energy-nbl-beats-q4-earnings-amp-revenue-estimates-cm1101789",
            "https://www.nasdaq.com/article/insiders-bullish-on-certain-holdings-of-jki-cm1101671",
            "https://www.nasdaq.com/article/occidentals-oxy-q4-earnings-amp-revenues-surpass-estimates-cm1098783",
            "https://www.nasdaq.com/article/noble-energy-to-reward-investors-with-more-than-500-mln-cash-flow-target-20190219-00935"
           ]


for url, name in zip(call_url, company_list):
  article_data = []
  html = urlopen(url)
  soup = BeautifulSoup(html, 'lxml')
  content_tags = soup.find_all('p')
  for text in content_tags:
    text = (BeautifulSoup(str(text),"lxml").get_text()).strip()
    if(text not in ['', '\n', '\t']):
      article_data.append(text)
  totalcontent = ','.join(article_data)
  #print(','.join(article_data))
  #Removing Non-Alphabetical Data, Stop Words And Perform Stemming
  from nltk.corpus import stopwords
  from nltk.stem.porter import PorterStemmer
  ps = PorterStemmer()
  corpus = []
  #Removing Non-Alphabetical Data
  review = re.sub('[^a-zA-Z]', ' ', totalcontent)
  review = review.lower()
  review = review.split()
  #Removing Stop Words And Perform Stemming
  review = [ps.stem(word) for word in review if word not in set(stopwords.words('english'))] #Making the list as set so that algorithm can run faster
  #Join all the words to create one string
  review = ' '.join(review)
  corpus.append(review)
  #Bag Of Words    
  from sklearn.feature_extraction.text import CountVectorizer
  cv = CountVectorizer()
  sparceMatrix = cv.fit_transform(corpus)
  featureset = sparceMatrix.toarray()
  #Sentiment ANalysis
  analysis = TextBlob(corpus[0])
  sentiment_val = analysis.sentiment.polarity
  print(sentiment_val)
  
  if(sentiment_val > 0.1):
    print(name+' has a positive latest')
  else:
    if(sentiment_val < 0):
      print(name+' has a negative latest news')
    else:
      print(name+' has a normal latest news')

#------------------Data Analytics------------------#
