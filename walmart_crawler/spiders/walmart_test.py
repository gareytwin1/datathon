from scrapy import Selector 
import requests 

url = "https://www.walmart.com/search/?query=Food&redirect=false"
html = requests.get(url).content
sel = Selector(text=html)

#top_products = sel.css("div.wpa-brand-products ::text").extract()
#print(f"---------top products-------------")
#print(top_products)

#titles = top_products[::7]
#prices = top_products[2::7]
#ratings = top_products[1::7]

#product_prices = [float(price.replace("$","")) for price in prices]
#product_dict = {k:[price, url] for k, price in zip(titles, product_prices)}

search_products = sel.css("div.search-product-result ::text").extract()
products = [product.strip().lower() for product in search_products[1:]]

titles = []
ratings = []
prices = []
for i, v in enumerate(products):
    if v == "product title": titles.append(products[i+1].title())
    if v == "average rating:": ratings.append(float(products[i+2]))
    if v == "current price": prices.append(float(products[i+1].replace("$","")))

search_product_dict = {title: (rating,price,url) for title,rating,price in zip(titles,ratings,prices)}
print("---------search product dictionary----------")
for k, v in search_product_dict.items():
    print(f"{k}: {v}")
