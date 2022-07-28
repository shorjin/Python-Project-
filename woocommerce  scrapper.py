from requests_html import HTMLSession
import csv
import pandas as pd
#思路：get url ,then get page item to extract item information
url='https://barefootbuttons.com/product-category/version-1/'
s = HTMLSession()
# use session to get the url
r = s.get(url)
#use css selector or xpath,find whatever element .find header 在这个page，主要看下page是否loading.# 表示id
print(r.html.find('#header'))
# remove 'box' 后面的空格，box 和small当中有个gap，我用. means our cs selector is looking for a div tag where
#class name matches product-small 和box
items=r.html.find('div.product-small.box')
items[0].find('a',first=True).attrs['href']
print(items[2].find('a',first=True).attrs['href'])

#使用方程获得所有的产品网址,return links as a list
from requests_html import HTMLSession
url = 'https://barefootbuttons.com/product-category/version-1/'
s = HTMLSession()
#把r = s.get(url) 放到loop里，#第一次出现的true number,我们在搜索在我们items的list里，每次a tag里的，只要attribute 是herf的内容
def get_links(url):
    r = s.get(url)
    items = r.html.find('div.product-small.box')
    links = []
    for item in items:
        links.append(item.find('a',first=True).attrs['href'])
        #注意这里要return links 不要 return item,而且这个return对应方程
    return links
print(len(get_links(url)))

#思路：有了搜索页面每个商品的link，然后通过这个link 再爬虫商品的具体信息，先测试一个商品
def get_product(links):
    r=s.get(links)
    title=r.html.find('h1',first=True).full_text.strip()
    #注意看价格起始是再bdi下面的，为了更好定位在上面一个class：woocommerce-Price-amount.amount，定位好,再amount后面放个space bdi 表示搜索bdi下面的第一个child matching 这个tag,但是这个方法失败了提取的数字是0
    #因为这个页面起始有很多dbi，第一个bdi对应的价格是0,remove first =TRUE 放index[1]
    price = r.html.find('span.woocommerce-Price-amount.amount bdi')[1].full_text.strip()
    #sku所对应的class是 span,first=True only returns the first Element found
    sku = r.html.find('span.sku',first=True).full_text
    #我要找a tag 下面的attribute 所以开[]，我要search within attribute of the tag
    tag=r.html.find('a[rel=tag]',first=True).full_text
    #别忘记空格都要换成.本来是p tag,class=p.stock in-stock 代码需要把 p.stock in-stock，stock 和in—stock当中的空格替换为p.stock.in-stock
    try:
        stock = r.html.find('p.stock.in-stock', first=True).full_text
    except:
        stock = 'no stock'

    #print(title,price,sku,tag,stock)
    #创建dictionary
    product={
        'title':title,
        'price':price,
        'SKU':sku.strip(),
        'Tag':tag.strip(),
        'Stock_status':stock.strip()
    }
    print(product)
    return product
#links='https://barefootbuttons.com/product/v1-mini-red/'
#get_product(links)

#put all together
links=get_links(url)
results=[]
for link in links:
    #运行get_products 方程
    results.append(get_product(link))

#储存csv文件，新建csv名字为results，open it as a white file,encoding 和 newline 一定要放，不然可能打不开
with open('results.csv','w',encoding='utf8',newline='')as f:
    #write dictionary to csv文件，f表示file 就是上面的f，这个文件的column 名字是dict的第一条数据的key
    wr=csv.DictWriter(f,fieldnames=results[0].keys(),)
    #write header
    wr.writeheader()
    #write rows in our results rows
    wr.writerows(results)
print('Finish')