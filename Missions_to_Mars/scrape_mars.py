#import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
# for pause
import time
# to format URLs
from urllib.parse import urlsplit

def scrape():
    browser = Browser("chrome", headless=False)

    # set url to NASA news site and visit with splinter
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # get html from splinter and give to BeautifulSoup
    html = browser.html
    page_to_parse = bs(html,"html.parser")
    # use soup to pull first article title and paragraph
    news_title = page_to_parse.find("div",class_="content_title").find("a").text
    news_p = page_to_parse.find("div", class_="article_teaser_body").text
    ############################################################################################################
    # set link to get jpl image, send splinter to fetch
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    #Getting the base url
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
    #Design an xpath selector to grab the image
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"
    #Use splinter to click on the mars featured image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = base_url + img_url

    # visit the JPL website and scrape the featured image

 #  set link to get jpl image, send splinter to fetch
  #     jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
  #     browser.visit(jpl_image_url)
  #     # give page time to load
    #    time.sleep(1)
    #    # navigate browser to full size image
  #     browser.click_link_by_partial_text('FULL IMAGE')
    # give page time to load
 #     time.sleep(1)
  #     browser.click_link_by_partial_text('more info')
  #     # give page time to load
  #     time.sleep(1)
  #     # get html from splinter and give to BeautifulSoup
  #     html = browser.html
  #     page_to_parse = bs(html,"html.parser")
  #     # find image url with soup
   #    img_src = page_to_parse.find('img', class_='main_image').get('src')
   #    # get the base url
   #    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(jpl_image_url))
   #    # put them together
  #     featured_image_url=base_url + img_src

    ############################################################################################################
    #get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    tweet_xpath='//*[@id="stream-item-tweet-1164580766023606272"]/div[1]/div[2]/div[2]/p'
    mars_weather  = browser.find_by_xpath(tweet_xpath).text
    ############################################################################################################
    # get mars facts
    #url_facts = "https://space-facts.com/mars/"
    #table = pd.read_html(url_facts)
    #table[1]
    #df_mars_facts = table[1]
    #df_mars_facts.columns = ["Parameter", "Values"]
    #df_mars_facts.set_index(["Parameter"])
    #df_mars_facts = df_mars_facts.to_html()

    # get mars facts
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)
    #import table into df, make df into table ... ok
    df = mars_table[1]
    df.columns = ['Property', 'Value']
    df.set_index('Property', inplace=True)
    mars_facts = df.to_html()
    ############################################################################################################
    # go to USGS Astrogeology get html
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # get the base url
    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url))
    browser.visit(url)
    html = browser.html
    page_to_parse = bs(html,"html.parser")
    # collect titles and links to hemisphere_image_urls
    hemisphere_image_urls = []
    hemisphere_image_urls_titles = []
    hemisphere_image_urls_images = []
    img_urls = []
    # collect container divs with links and titles
    item_div = page_to_parse.find_all('div', class_='item')
    # iterate through containers
    for item in item_div: 
    # grab title
        title = item.find('h3').text
    # collect links
        img_urls.append(item.find('a', class_='product-item')['href'])
        hemisphere_image_urls_titles.append(title)
    # visit collected links to gather large image links
    for link in img_urls:
        browser.visit(base_url + link)
        img_html = browser.html
        page_to_parse = bs(img_html, 'html.parser')
    # collect links
        full_img_url = base_url + page_to_parse.find('img', class_='wide-image')['src']
        hemisphere_image_urls_images.append(full_img_url)
    for url, title in zip(hemisphere_image_urls_images, hemisphere_image_urls_titles):
        hemisphere_image_urls.append({"title" : title, "img_url" : url})
    # make dictionary out of all collected data for use in flask app
    mars_info={"news_title":news_title,
            "news_p":news_p,
            "featured_image_url":featured_image_url,
            "tweet_url":url_weather,
            "mars_weather":mars_weather,
            "mars_facts":mars_facts,
            "hemisphere_image_urls":hemisphere_image_urls    
            }
    browser.quit()
    return mars_info