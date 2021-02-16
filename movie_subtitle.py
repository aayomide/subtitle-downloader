#!/usr/bin/env python
# coding: utf-8

# README.md
# ## Download movie subtitle
# Automated the download of movie subtitles from Netnaija
# 
# ## Usage
# `python movie_subtitle.py <movie_name>`

import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import sys

# url to the movie
search_item = str(sys.argv[1])
url = 'https://www.thenetnaija.com/search?t=' + search_item

# connect to search results webpage
search_url = requests.get(url)

if search_url.status_code == 200: 
    print('Search results fetched ...')
    search_content = search_url.content
    search_soup = BeautifulSoup(search_content, 'html.parser')
    
    # select only results that start with 'Movie:' as other kind of videos contain the search item value
    for result_title in search_soup.select('.result-title'):
        result_title_text = result_title.text
        if re.match('^Movie:', result_title_text):
            first_movie_title = result_title_text.split(':', 1)[1]
            print(f'Found your movie: {first_movie_title}')
            movie_link = result_title.select('a')[0].get('href')
            break
else:
    print('Troubles connecting to the webpage')
# webbrowser.open_new_tab(movie_link)

#Next, select the movie link and navigate to the movie page 
movie_url = requests.get(movie_link)
print(f'Fetching {first_movie_title} movie page ...')

if movie_url.status_code == 200: 
    try:
        print(f'Currently on {first_movie_title} movie page...')
        movie_page_content = movie_url.content
        movie_page_soup = BeautifulSoup(movie_page_content, 'html.parser')

        # select the movie subtitle link and open the subtitle download page on the webbrowser
        subtitle_link = movie_page_soup.select('.button.download')[2].get('href')
        print('Opening subtitle download link ...')
        webbrowser.open_new_tab(subtitle_link)
    
    except:
        print("Ooops! No subtitle for this movie yet on Netnaija")