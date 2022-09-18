from flask import (
    Flask, 
    render_template,
    request
)

import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        channel_name = 'https://www.youtube.com/' + request.form['search_query']

        # Check if page returns status code 200
        response = requests.get(channel_name)
        status = response.status_code

        if status == 200:
            options = Options()
            options.add_argument('--headless') # headless is to avoid pop up browser
            driver = webdriver.Chrome('C:\chromedriver.exe', options=options)  
            driver.get(channel_name)

            html = driver.page_source

            soup = BeautifulSoup(html, 'lxml')
            html_text = soup.find_all('a', {'class', 'yt-simple-endpoint style-scope ytd-grid-video-renderer'}, href=True)

            titles = []
            for a in html_text:
                titles.append([a.text, 'https://www.youtube.com/' + a['href']])

            titles_unique = []
            for title in titles:
                if title not in titles_unique:
                    titles_unique.append(title)

        else:
            titles_unique = ''

        return render_template('index.html', status=status, channel_name=channel_name, html_text=titles_unique)

    return render_template('index.html', channel_name='')

