from bs4 import BeautifulSoup 
import requests
from lxml.html import fromstring
import time 
import json

# Getting Rotating Proxies
def get_proxies():
    url = 'http://www.freeproxylists.net/?c=US'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Getting  up IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

# Getting HTML Content
def get_html():
	URL = "https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1"
	r = requests.get(URL,proxies=get_proxies())
	time.sleep(3)
	soup = BeautifulSoup(r.content, 'html5lib') 
	return soup

# Creating List of Dictionary to Finalise Output in JSON
def get_list_of_dict(soup,list_of_dict):
	Price=soup.select('div#Div1 span.price')
	Title = soup.select('div#Div1 a.catalog-item-name')
	Status=soup.select('div#Div1 span.status')
	Manufacturer=soup.select('div#Div1 a.catalog-item-brand')

	for i in range(len(Price)):
		boolean=True
		if Status[i].text=="Out of Stock":
			boolean=False
		list_of_dict.append({'price':float(Price[i].text[1:]),'title':Title[i].text,'status':boolean,'maftr':Manufacturer[i].text})
	return json.dumps(list_of_dict)

#Driver Code 
if __name__=="__main__":
	get_proxies()
	soup=get_html()
	list_of_dict=list(dict())

	print(get_list_of_dict(soup,list_of_dict))




