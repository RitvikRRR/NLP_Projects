from nltk.tokenize import sent_tokenize
import requests
from bs4 import BeautifulSoup
import urllib.request
import re

start_url= "https://www.espn.com/"
r = requests.get(start_url)
data = r.text
soup = BeautifulSoup(data, "html.parser")

with open('urls.txt', 'w') as f:
  url_list = f.read().splitlines()
  for u in url_list:
    print(u)

with open('urls.txt', 'w') as f:
    for link in soup.find_all('a'):
        print(link.get('href'))
        f.write(str(link.get('href')) + '\n\n')
        lnk_str = str(link.get('href'))
        print(lnk_str)
        if 'Sports' in lnk_str or 'sports' in lnk_str:
            if lnk_str.startswith('/url?q='):
                lnk_str = lnk_str[10:]
                print('MOD:', lnk_str)
            if lnk_str.startswith('http') and 'google' not in lnk_str:
                f.write(lnk_str + '\n')
            if '&' in lnk_str:
                i = lnk_str.find('&')
                lnk_str = lnk_str[:i]
            

with open('urls.txt', 'r') as f:
    url_list = f.read().splitlines()
for u in url_list:
    print(u)

def vis(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

req = urllib.request.Request(start_url, headers={})
with open('urls.txt', 'r') as input:
    for (counter, line) in enumerate(input):
        with open('filename{0}.txt'.format(counter), 'w') as output:
            soup = BeautifulSoup("html.parser")
            data = soup.findAll(text=True)
            result = filter(vis, data)
            temp_list = list(result)
            temp_str = ' '.join(temp_list)