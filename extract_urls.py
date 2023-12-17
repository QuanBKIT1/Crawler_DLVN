import requests
from bs4 import BeautifulSoup

with open('out.html', 'r', encoding='utf-8') as file:
        html_doc = file.read()
soup = BeautifulSoup(html_doc, 'html.parser')
elements = soup.select('.mda-box-name ')
with open('urls.txt', 'w') as file:
    for element in elements:
          file.write(element.get('href')+'\n')