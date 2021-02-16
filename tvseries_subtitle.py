#!/usr/bin/env python
# coding: utf-8

# README.md
# ## Download TV series subtitles
# Automated the download of tv series
# 
# ## Usage
# 
# python tvseries_subtitle.py <tvseries_name> <tvseries_season number>`


import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import sys

try:
    # Python 3.x
    from urllib.request import urlopen, urlretrieve, quote
    from urllib.parse import urljoin
except ImportError:
    # Python 2.x
    from urllib import urlopen, urlretrieve, quote
    from urlparse import urljoin

user_search = str(sys.argv[1])
season = int(sys.argv[2])
payload = {'q': user_search}  # q is the name of the input field .. vikings is the search item

base_url = 'http://www.tvsubtitles.net/'
search_url = 'http://www.tvsubtitles.net/search.php'

# connect to webpage url
def page_content(url, parameters):
    """ Connect to the webpage and parse its content
    attributes: url - webpage link
                parameters - additional details to add to the web link (optional)
    
    """
    response = requests.get(url, params=parameters)
    search_content = response.content
    search_soup = BeautifulSoup(search_content, 'html.parser')
    return search_soup

search_page_content = page_content(search_url, payload)
print('Search results fetched ...')

# select the tv series link in the search result
series_partial_link = search_page_content.select('.left_articles')[0].select('a')[0].get('href')
series_full_link = base_url + series_partial_link
series_full_link_by_season =  series_full_link[:-5] + '-{}'.format(str(season)) + series_full_link[-5:]
# print(series_full_link_by_season)

# Navigate to the tv series webpage
series_page_content = page_content(series_full_link_by_season, None)
print('Currently on the series page ...')

# get the tv series season subtitle link
subtitle_partial_link = series_page_content.select('table')[0].select('tr')[-1].select('a')[1].get('href')
subtitle_full_link = base_url + subtitle_partial_link


# Navigate the subtitle webpage
subtitle_page_content = page_content(subtitle_full_link, None)
print('Successully landed on the subtitle page ...')

# select the download link and open in the webbrowser
# opening the page automatically downloads the subtitle file
for a_tag in subtitle_page_content.select('a'):
    link = a_tag.get('href')
    if link:
        if link.startswith('download'):
            final_link = base_url + link
            s = requests.Session()
            get_file = s.get(final_link, verify='False')
            print('Fetching subtitle ...')
            webbrowser.open_new_tab(final_link)