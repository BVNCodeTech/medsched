import requests
import re


# Command takes in the unformatter medicine name and returns a *DICTIONARY* of names and prices (which are lists)
def get_medicines(query):
    if ' ' in query:
        query = query.replace(' ', '+')

    content = requests.get(f'https://pharmeasy.in/search/all?name={query}').text
    prices = re.findall(r'₹<!-- -->(\S{5})', content)
    names = []
    for i in range(content.count('<h1 class="ooufh">')):
        index = content.index('<h1 class="ooufh">')
        name = content[index:index+50].split('<')
        names.append(name[1].split('>')[1])
        content = content[index+18:]

    return {"names":names, "prices":prices}