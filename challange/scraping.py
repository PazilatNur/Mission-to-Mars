from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # hemispheres_images_urls = hemisphere_data(browser)
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
    #   "hemispheres dict": {"hemispheres links": hemispheres_images_urls}
}

    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

# def hemisphere_data(browser):
#     url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     browser.visit(url)
#     browser.is_element_present_by_css('div.list_text', wait_time=1)
#     html=browser.html
#     img_soup= soup(html, "html.parser")
#     tag_box=img_soup.find('div', class_='collapsible results')
#     tags=tag_box.find_all('div', class_='item')
#     full_url_list=[]
#     hemispheres_images_urls=[]
    
#     try:
#         for tag in tags:
#             img_url=tag.find('a', class_="itemLink product-item").get('href')
#             full_url_list.append(f'https://astrogeology.usgs.gov/{img_url}')

#         for url in full_url_list:
#             hemispheres = {}
#             browser.visit(url)
#             html = browser.html
#             full_image_soup = soup(html, 'html.parser')
#             full_link=full_image_soup.find('img',class_='wide-image').get('src')
#             image_title=full_image_soup.find('h2', class_='title').text
#             # print(full_link,image_title)
#             hemispheres["img_url"]=full_link
#             hemispheres["title"]=image_title
#             hemispheres_images_urls.append(hemispheres)
    
#     except AttributeError:
#         return None
    
#     return hemispheres_images_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
