import requests
import re


# Command takes in the unformatter medicine name and returns a *DICTIONARY* of names and prices (which are lists)
def get_medicines(query):
    if ' ' in query:
        query = query.replace(' ', '+')
    print(f'https://pharmeasy.in/search/all?name={query}')
    content = requests.get(f'https://pharmeasy.in/search/all?name={query}').text

    prices = re.findall(r'₹<!-- -->(\S{5})', content)
    names = []
    src = []
    for i in range(content.count('<h1 class="ooufh">')):
        index = content.index('<h1 class="ooufh">')
        src_index = content.index('alt="medicine" src="')
        name = content[index:index+50].split('<')
        link = content[src_index:src_index+100].split('"')
        names.append(name[1].split('>')[1])
        src.append(link[2])
        content = content[index+18:]
        print(src)

    return {"names":names, "prices":prices, "image links":src}

get_medicines('indocap sr')
