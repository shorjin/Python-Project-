from requests_html import HTMLSession

#single page to get price and title
def getPrice(url):
    # get session first
    s = HTMLSession()
    # use session to get the url
    r = s.get(url)
    # magic line
    r.html.render(sleep=1)
    #create product dict,title 所在的那个class copy xpath,r.html.xpath(''),引号里面复制xpath内容,另外注意dict 两个内容当中逗号分开
    #first=True means we make sure that we found the first element
    product={
        'title': r.html.xpath('//*[@id="productTitle"]',first=True).text,
        'price': r.html.xpath('//*[@id="corePrice_desktop"]/div/table/tbody/tr[2]/td[2]/span[1]/span[1]',first=True).text
    }
    print(product)
    return product

getPrice('https://www.amazon.com/2021-Apple-10-2-inch-iPad-Wi-Fi/dp/B09G9CJM1Z/ref=sr_1_3?keywords=ipad&qid=1658772017&sr=8-3')


#compare two links

urllist=['https://www.amazon.com/2021-Apple-11-inch-Wi%E2%80%91Fi-256GB/dp/B093229FHR/ref=sr_1_10?crid=133CCF0MESED0&keywords=ipad&qid=1658771644&sprefix=ipad+%2Caps%2C81&sr=8-10',
         'https://www.amazon.com/2022-Apple-iPad-10-9-inch-Wi-Fi/dp/B09V3HN1KC/ref=sr_1_3?crid=35H414GU0K7TB&keywords=ipad+2022&qid=1658767756&sprefix=ipad+2022%2Caps%2C91&sr=8-3',

         ]
def getPrice(url):
    # get session first
    s = HTMLSession()
    # use session to get the url
    r = s.get(url)
    # magic line
    r.html.render(sleep=1)
    #create product dict,title 所在的那个class copy xpath,r.html.xpath(''),引号里面复制xpath内容,另外注意dict 两个内容当中逗号分开
    #first=True means we make sure that we found the first element
    product={
        'title': r.html.xpath('//*[@id="productTitle"]',first=True).text,
        'price': r.html.xpath('//*[@id="corePrice_desktop"]/div/table/tbody/tr[2]/td[2]/span[1]/span[1]',first=True).text
    }
    print(product)
    return product
tvlist=[]
for url in urllist:
    tvlist.append (getPrice(url))
print(len(tvlist))