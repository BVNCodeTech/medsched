import requests
import re


def get_medicines(query):
    if ' ' in query:
        query = query.replace(' ', '+')
    content = requests.get(f'https://pharmeasy.in/search/all?name={query}').text
    print(content)
    prices = re.findall(r'₹<!-- -->(\S{5})', content)
    names = []
    src = []
    for i in range(content.count('<h1 class="ooufh">')):
        index = content.index('<h1 class="ooufh">')
        try:
            src_index = content.index('alt="medicine" src="')
            link = content[src_index:src_index+100].split('"')
            src.append(link[2])
        except:
            pass # THEY FUCKING IP BLOCKED ME - NL
        name = content[index:index+50].split('<')
        names.append(name[1].split('>')[1])
        content = content[index+18:]

    return {"names":names, "prices":prices, "image links":src}

