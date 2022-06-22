
from splinter import Browser

# Parses the HTML
from bs4 import BeautifulSoup
import pandas as pd
import time

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Setup splinter
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set an empty dict for listings that we can save to Mongo
    mars = {}

    url = "https://redplanetscience.com/"
    
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)

    news_title = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[2]').text

    news_p = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[3]').text

    # Let it sleep for 1 second
    time.sleep(1)

    url = "https://spaceimages-mars.com/"
    
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)

    browser.find_by_xpath('/html/body/div[1]/div/a/button').click()

    featured_image_url = browser.find_by_xpath('/html/body/div[8]/div/div/div/div/img')['src']

    time.sleep(1)

    url = "https://galaxyfacts-mars.com/"
    
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)

    df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace = True)
    mars_table = df.to_html()
    
    time.sleep(1)

    url = "https://marshemispheres.com/"
    
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)

    hemisphere_image_urls =[]

    for i in range(1,5):
        hemis = {}
        x_path = '//*[@id="product-section"]/div[2]/div['+str(i)+']/a/img'
        browser.find_by_xpath(x_path).click()
        hemis['img_url']= browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')['href']
        hemis['title']= browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').text
        hemisphere_image_urls.append(hemis)
    
    
        browser.back()


    # Quit the browser
    browser.quit()

    mars = {'News_Title':news_title,
    'News_Paragraph':news_p,
    'Image':featured_image_url,
    'Mars_facts': mars_table,
    'hemispheres': hemisphere_image_urls




    }

    # Return our dictionary
    return mars