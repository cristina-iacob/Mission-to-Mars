# import and setup dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from urllib.parse import urlsplit
import time

def scrape():
    browser = Browser("chrome", headless=False)

    # NASA #######################################################################

    # visiting NASA Mars News Site
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    time.sleep(3)
    # get html from splinter and send it to beautifulsoup
    nasa_html = browser.html
    nasa_soup = bs(nasa_html,"html.parser")
    # use soup to pull title and paragraph for the first article
    news_title = nasa_soup.find("div",class_="content_title").find("a").text
    news_p = nasa_soup.find("div", class_="article_teaser_body").text

    # JPL #######################################################################

    # set link to get jpl image, send splinter to fetch
    jpl_url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url_image)
    time.sleep(1)
    # navigate browser to full size image
    browser.click_link_by_partial_text('FULL IMAGE')
    # give page time to load
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    # get image url using BeautifulSoup
    image_html = browser.html
    image_soup = bs(image_html, "html.parser")
    # get image url using BeautifulSoup
    image_url = image_soup.find('img', class_='main_image').get('src')
    # getting the base url
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(jpl_url_image))
    # full link
    featured_image_url = base_url + image_url


    # Twitter #######################################################################

    #get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    # get html from splinter and give to BeautifulSoup
    weather_html = browser.html
    weather_soup = bs(weather_html, "html.parser")
    mars_weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(mars_weather)

    #There is no weather data for 2 weeks so I'll use the previous info
    #We won’t be hearing from @MarsCuriosity or @NASAInSight for the next 2 weeks during Mars solar conjunction. Read more about why Mars missions go silent every 2 years: https://www.wral.com/mars-spacecraft-go-quiet-during-solar-conjunction/18595551/ …pic.twitter.com/fWruE2v151

    #tweet_xpath='//*[@id="stream-item-tweet-1164580766023606272"]/div[1]/div[2]/div[2]/p'
    #mars_weather  = browser.find_by_xpath(tweet_xpath).text
    #print(mars_weather)

    # Space-facts #######################################################################

    # visiting space-facts site
    url_facts = "https://space-facts.com/mars/"
    # read table 1 with pandas
    table = pd.read_html(url_facts)
    #ta1]ble[
    # rename columns
    df_mars_facts = table[1]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])
    # make df into table 
    mars_facts = df_mars_facts.to_html()
    #mars_html_table


    # USGS #######################################################################

    # visiting USGS site
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    # get html from splinter and give to beautiful soup
    time.sleep(2)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html,'html.parser')
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    # retreive all items that contain mars hemispheres information
    items = hemispheres_soup.find_all('div', class_='item')
    # Store the main_ul
    from urllib.parse import urlsplit
    hemispheres_main_url = "{0.scheme}://{0.netloc}".format(urlsplit(url_hemispheres))
    # loop through the items
    for i in items: 
        # Store title
        title = i.find('h3').text
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']   
        # go to full image  
        browser.visit(hemispheres_main_url + partial_img_url)  
        # get and parse individual hemisphere information
        partial_img_html = browser.html  
        hemispheres_soup = bs( partial_img_html, 'html.parser')   
        # get full image 
        img_url = hemispheres_main_url + hemispheres_soup.find('img', class_='wide-image')['src']
        # append title to each image
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

    ##################################################################################################
    ##################################################################################################

    # make dictionary out of all collected data for use in flask app
    mars_info={"news_title":news_title,
            "news_p":news_p,
            "featured_image_url":featured_image_url,
            "tweet_url":mars_weather,
            "mars_weather":mars_weather,
            "mars_facts":mars_facts,
            "hemisphere_image_urls":hemisphere_image_urls    
            }
    browser.quit()
    return mars_info






  