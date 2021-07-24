import requests
import re
from bs4 import BeautifulSoup


def get_medicines(query):
    if ' ' in query:
        query = query.replace(' ', '+')
    content = requests.get(f'https://pharmeasy.in/search/all?name={query}').text
    soup = BeautifulSoup(content, 'html.parser')

    names = []
    for h1 in soup.find_all('h1', class_='ooufh'):
        first = str(h1)[18:]
        names.append(first[:-5])

    prices = []
    for div in soup.find_all('div', class_='_1_yM9'):
        prices.append(str(div)[29:][:-7])

    links = []
    for a_tag in soup.find_all('a' ,href=True):
        if a_tag['href'].find('/online-medicine-order/') != -1 or a_tag['href'].find('/health-care-products/') != -1:
            links.append(f"https://pharmeasy.in{a_tag['href']}")

    return {'names':names, 'prices':prices, 'order links':links}
