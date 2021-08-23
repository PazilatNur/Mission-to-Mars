#!/usr/bin/env python
# coding: utf-8

# In[1]:
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
# In[2]:
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
# In[3]:
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)
# In[4]:
html=browser.html
news_soup=soup(html,"html.parser")
slide_elem = news_soup.select_one('div.list_text')
# In[5]

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title
# In[6]:

news_p=slide_elem.find('div', class_='article_teaser_body').get_text()
news_p
# Featured Images
# In[7]:
url = 'https://spaceimages-mars.com'
browser.visit(url)
# In[8]:
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()
# In[9]:
html=browser.html

img_soup= soup(html, "html.parser")
# In[10]:
img_url_rel = img_soup.find('img', class_="headerimage fade-in").get('src')
img_url_rel


# <img class="headerimage fade-in" src="image/featured/mars2.jpg">
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[14]:

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df

df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# In[16]:

df.to_html()

# In[17]:

browser.quit()


# In[ ]:
