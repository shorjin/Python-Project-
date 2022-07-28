#搜索页面
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#搜索页面
baseurl='https://www.thewhiskyexchange.com/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}
r=requests.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky')
soup=BeautifulSoup(r.content,'lxml')
#class 后面有个_ 千万别漏掉,一定要找link 上面的一个class
productlist=soup.find_all('li',class_='product-grid__item')
productlinks=[]
for item in productlist:
    for link in item.find_all('a',href=True):
        productlinks.append(baseurl+link['href'])
print(len(productlinks))



#搜索页面+翻页
#这个网页第一页24个商品，第二页14个商品，注意要把productlinks = []放在for loop 翻页方程外面，不然只会储存第二页爬虫的内容（14个商品）
baseurl='https://www.thewhiskyexchange.com/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}
productlinks = []
for i in range (1,3):
    r=requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={i}')
    soup=BeautifulSoup(r.content, 'lxml')
    #class 后面有个_ 千万别漏掉,一定要找link 上面的一个class
    productlist=soup.find_all('li', class_='product-grid__item')
    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl+link['href'])

print(len(productlinks))


#打开搜索页面的单个商品页面

testlink = 'https://www.thewhiskyexchange.com/p/29388/suntory-hibiki-harmony'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}
r = requests.get(testlink, headers=headers)
soup=BeautifulSoup(r.content, 'lxml')
#class那边的underscore千万别忘记，这个class是商品名称所对应的class
name = soup.find('h1',class_='product-main__name').text.strip()

price=soup.find('p',class_='product-action__price').text
review_score=soup.find('span',class_='review-overview__rating star-rating star-rating--40').text.strip()
review_count=soup.find('span',class_='review-overview__count').text.strip()
print(soup.find('span',class_='review-overview__count').text.strip())
whisky = {
    'name':name,
    'rating':review_score,
    'review':review_count,
    'price':price}







pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)





#全部放在一起
baseurl='https://www.thewhiskyexchange.com/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}
name=[]
productlinks=[]
review_score=[]
review_count=[]
price=[]
whiskylist=[]

for i in range (1,3):
    r=requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={i}',headers=headers)
    soup=BeautifulSoup(r.content, 'lxml')
    #class 后面有个_ 千万别漏掉,一定要找link 上面的一个class
    productlist=soup.find_all('li', class_='product-grid__item')
    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl+link['href'])

#print(productlinks)

for link in productlinks:

    r = requests.get(link, headers=headers)
    soup=BeautifulSoup(r.content, 'lxml')
    #class那边的underscore千万别忘记，这个class是商品名称所对应的class
    name = soup.find('h1',class_='product-main__name').text.strip()

    price=soup.find('p',class_='product-action__price').text
    #这里要注意哦，class_='review-overview__rating star-rating star-rating--40'有的商品下面这个class 名字不是40，是30 这样我就没办法提取text
    #需要更改，在这个class上面在找个
    #review_score=soup.find('span',class_='review-overview__rating star-rating star-rating--40').text.strip()
    #我把它换成包含所有class的，then that will help us when writing has changed
    #try:
        #review_score = soup.find('div', class_='review-overview__rating star-rating star-rating--.*?').text.strip()
    #except:
        #review_score='no rating'
    try:
        review_count=soup.find('span',class_='review-overview__count').text.strip()

    except:
        review_count='no reviews'

    whisky = {
        'name':name,
        'rating':review_score,
        'review':review_count,
        'price':price}
    #print(whisky)
    print('saving: ',whisky['name'])
#change print to data frame
    whiskylist.append(whisky)

df=pd.DataFrame(whiskylist)
print(df)