import requests
from bs4 import BeautifulSoup
import pandas as pd

#url='https://www.ebay.com/sch/i.html?_from=R40&_nkw=%E2%80%98skydio%E2%80%99&_sacat=0&LH_TitleDesc=0&_fsrp=1&LH_Auction=1&rt=nc&LH_PrefLoc=1&LH_Complete=1&LH_Sold=1&_pgn=1'
search_term=input('Please input the data you want to search(use plus to substitute space: ')
#search_term='sony+6400'
def get_data(search_term):
    url = f'https://www.ebay.com/sch/i.html?_fsrp=1&_from=R40&_nkw={search_term}&_sacat=0&LH_Sold=1&rt=nc&LH_Auction=1&_pgn=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(url)
    return soup


def parse(soup):
    #after test add an empty list
    productslist=[]
    #li class 下面的 div srp-river-results clearfix
    results = soup.find('div', {'class': 'srp-river-results clearfix'}).find_all('li',{'class':'s-item s-item__pl-on-bottom'})
    for item in results:
        products = {
            'title': item.find('h3', {'class': 's-item__title s-item__title--has-tags'}).text,
            # replace 符号$to '',还有replace 千位数分隔号 to ‘’
            'soldprice': item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',','').strip(),
            # 在span tag下先找到s-item__title--tagblock的class 然后再找 另一个span tag，基本思路finding A element then within A element finding B element
            'solddate': item.find('div', {'class': 's-item__title--tagblock'}).find('span', {'class': 'POSITIVE'}).text,
            # span tag下的s-item__bids s-item__bidCount，我们可以只保留 s-item__bids 空格后面的都不要
            'bids': item.find('span', {'class': 's-item__bids'}).text,
            # 网上显示：<a target="_blank" data-s-d83m029="{&quot;eventFamily&quot;:&quot;LST&quot;
            #  class="s-item__link" href="https://www.ebay.com/itm/284905147960?epid=15042215977&amp;hash=item4255ab8e38%3Ag%3A79sAAOSwBjti2aKR&amp;LH_Auction=1">
            #  <h3 class="s-item__title s-item__title--has-tags">Skydio 2 Camera Drone + Cinema Upgrade Kit - Barely Flown</h3><span class="clipped">Opens in a new window or tab</span></a>
            # 我想获取tag a 下的 s-item__link其属性为href的内容
            'link': item.find('a', {'class': 's-item__link'})['href']
        }
        #test 需要打印
        #print(products)
        productslist.append(products)
    return productslist

def output(productslist,search_term):
    product_df=pd.DataFrame(productslist)
    product_df.to_csv(search_term+'output.csv',index=False)
    print('finished')
    return



# 运行get_data 方程，然后返回的内容命名soup
soup = get_data(search_term)
# 运行parse 方程，parameter 是上面那个方程return的soup

productslist=parse(soup)
output(productslist,search_term)