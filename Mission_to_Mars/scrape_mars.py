from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # create mars_data dict that we can insert into mongo
    mars_data = {}

    ################################################################################
    # Scrape mars.nasa.gov/news/
    ################################################################################
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
   
    # Parse HTML with Beautiful Soup
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')
    latest_slide = news_soup.select_one("li.slide")
    latest_slide.find('div', class_='content_title')

    # Retrieve the title in the latest news slide
    news_title = latest_slide.find('div', class_='content_title').get_text()
    news_para = latest_slide.find('div', class_='article_teaser_body').get_text()
    
    ##################################################################################
    # Scrape JPL Mars Space Images - Featured Image
    ##################################################################################
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)
    
    # Parse HTML with Beautiful Soup
    images_html = browser.html
    image_soup = BeautifulSoup(images_html, 'html.parser')
    img_url = image_soup.find('img', class_="headerimage fade-in")['src']

    # Use Base URL to obtain absolute URL
    featured_image_url = f" {image_url}/{img_url}"

    ##################################################################################
    # Scrape Space Facts url
    ##################################################################################
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    # facts_html = browser.html
    
    # Parse HTML with Beautiful Soup
    # fact_soup = BeautifulSoup(facts_html, 'html.parser')

    mars_fact_table = pd.read_html(mars_facts_url)
    mars_fact_df = mars_fact_table[0]
    mars_fact_df.columns = ['Description', 'Data']
    mars_facts_html_table = mars_fact_df.to_html()
    mars_facts_html_table.replace('\n', '')

    ##################################################################################
    # Scrape  USGS Astrogeology url
    ##################################################################################
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    
    # Parse HTML with Beautiful Soup
    # usgs_html = browser.html
    # usgs_soup = BeautifulSoup(usgs_html, 'html.parser')

    hemisphere_image_urls = []

    # Get Hemispheres list
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
        # Iterate through hemisphere information
        browser.find_by_css("a.product-item h3")[item].click()
    
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        # Find Sample Image Anchor Tag & Extract <href>
        sample_image = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_image["href"]
    
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        hemisphere_image_urls
        # Back to main page
        browser.back()

        

    ###################################################################################
    # Store Mars data in a dictionary
    ###################################################################################

    mars_data = {
        'news_title': news_title,
        'news_p': news_para,
        'featured_image_url': featured_image_url,
        'mars_facts_html_table': mars_facts_html_table,
        'hemisphere_image_urls' : hemisphere_image_urls
    }


    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

