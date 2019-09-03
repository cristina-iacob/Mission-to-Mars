#import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser

def scrape():
	browser = Browser("chrome", headless=False)

	#NASA Mars News url:
	news_url = "https://mars.nasa.gov/news/"
	browser.visit(news_url)

	# get html from splinter and give to BeautifulSoup
	html = browser.html
	page_to_parse = bs(html,"html.parser")

	# use soup to pull first article title and paragraph
	news_title = page_to_parse.find("div",class_="content_title").find("a").text
	news_p = page_to_parse.find("div", class_="article_teaser_body").text

	# set link to get jpl image, send splinter to fetch
	url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url_image)

	#Getting the base url
	from urllib.parse import urlsplit
	base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
	print(base_url)

	#Design an xpath selector to grab the image
	xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

	#Use splinter to click on the mars featured image
	#to bring the full resolution image
	results = browser.find_by_xpath(xpath)
	img = results[0]
	img.click()

	#get image url using BeautifulSoup
	html_image = browser.html
	soup = bs(html_image, "html.parser")
	img_url = soup.find("img", class_="fancybox-image")["src"]
	full_img_url = base_url + img_url
	print(full_img_url)

	#get mars weather's latest tweet from the website
	url_weather = "https://twitter.com/marswxreport?lang=en"
	browser.visit(url_weather)

	tweet_xpath='//*[@id="stream-item-tweet-1164580766023606272"]/div[1]/div[2]/div[2]/p'
	mars_weather  = browser.find_by_xpath(tweet_xpath).text
	print(mars_weather)

	url_facts = "https://space-facts.com/mars/"

	table = pd.read_html(url_facts)
	table[1]

	df_mars_facts = table[1]
	df_mars_facts.columns = ["Parameter", "Values"]
	df_mars_facts.set_index(["Parameter"])

	mars_html_table = df_mars_facts.to_html()
	mars_html_table = mars_html_table.replace("\n", "")
	mars_html_table

	# go to USGS Astrogeology get html
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url))
	base_url

	browser.visit(url)
	html = browser.html
	parsed_hemis = bs(html,"html.parser")

	hemisphere_image_urls = []
	hemisphere_image_urls_titles = []
	hemisphere_image_urls_images = []
	img_urls = []

	item_div = parsed_hemis.find_all('div', class_='item')

	for item in item_div: 

	    title = item.find('h3').text

	    img_urls.append(item.find('a', class_='product-item')['href'])
	    hemisphere_image_urls_titles.append(title)

	for link in img_urls:
	    browser.visit(base_url + link)
	    img_html = browser.html
	    parsed_hemis = bs(img_html, 'html.parser')
	    
	    full_img_url = base_url + parsed_hemis.find('img', class_='wide-image')['src']
	    hemisphere_image_urls_images.append(full_img_url)
	    
	for url, title in zip(hemisphere_image_urls_images, hemisphere_image_urls_titles):
	    hemisphere_image_urls.append({"title" : title, "img_url" : url})
	    
	#print title: image    
	#hemisphere_image_urls  
	mars_info={"news_title":news_title,
            "news_p":news_p,
            "featured_image_url":featured_image_url,
            "tweet_url":url_weather,
            "mars_weather":mars_weather,
            "mars_facts":mars_html_table,
            "hemisphere_image_urls":hemisphere_image_urls    
            }
    browser.quit()
    return mars_info 





