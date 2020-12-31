import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime



def item_exists(string):
    b = str(string)
    pattern = re.compile("(db_rs\/.+\/view)")
    item_search = re.search(pattern, b)
    if item_search:
        line = str(item_search.group())
        remove_prefix = line[6:]
        item = remove_prefix[:remove_prefix.__len__()-5]
        return item
    else:
        return None

def get_items(string):
    item_search_re = '(db_rs\/.+\/view)'
    item_search = re.search(item_search_re, string)
    return item_search

def get_object_id(string):
    string = str(string)
    object_id_search_re = '(obj=\d+)'
    obj_id_search = re.search(object_id_search_re, string)
    if obj_id_search:
        obj_id = obj_id_search.group()[4:]
        return obj_id
    else:
        return None

def clean_name(name):
    name = name.replace("+", " ")
    name = name.replace("%", "")
    return name

if __name__ == "__main__":

    item_db_size = 49502

    ge_top_100 = 'https://secure.runescape.com/m=itemdb_rs/top100?list=2&scale=0'
    snowverload = 'https://secure.runescape.com/m=itemdb_rs/Snowverload+plush+token/viewitem?obj=41345'

    s = requests.Session()
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    r = s.get(ge_top_100, headers=headers, cookies={'from-my': 'browser'})
    bs = BeautifulSoup(r.text, 'html.parser')

    title = bs.title
    description = bs.title.string
    html = bs.find_all('a')

    item_prices = dict()
    item_names = []
    html_idx = []

    #identify names and ids
    for i in html:
        if i.attrs['href']:
            id = get_object_id(i.attrs['href'])
            name = item_exists(i.attrs['href'])
            if name and id:
                html_idx.append(html.index(i))
                item_names.append(name)
                #name = clean_name(name)
                item_prices[id] = name, []

    #build search string
    giant_re = '(db_rs\/.+\/view.*obj=\d+)((.*\+\d\d%<)|(.*\d+.\d[a-z]<))'
    name_re = '(db_rs\/.+\/view)'
    id_re = '(obj=\d+.)'
    #data_re = '(\d+.\d[a-z]*<)'
    data_re = '(\d+.\d[a-z]*<)|(\+\d\d%)'
    giant_re_matches = 0
    matches = 0

    for line in html:
        string = str(line)
        search = re.search(giant_re, string)
        name = None
        data = None
        item_id = None
        if search:
            giant_re_matches +=1
            search = search.group()
            #print(search)
            search1 = re.search(name_re, search)
            if search1:
                search1 = search1.group()
                name = search1[6:search1.__len__()-5]

            search2 = re.search(id_re, search)
            if search2:
                search2 = search2.group()
                item_id = search2[4:search2.__len__()-1]

            search3 = re.search(data_re, search)
            if search3:
                search3 = search3.group()
                data = search3[:search3.__len__()-1]

            #new_item = (name, item_id, data)
            #print("{0}:{1}:{2}".format(name, item_id, data))
            if item_id and data:
                matches +=1
                item_prices[item_id][1].append(data)

    now = datetime.now()
    fn = "./data/prices-{0}-{1}-{2}-{3}.json".format(now.year,now.month, now.day, now.strftime("%H:%M:%S"))
    json.dump(item_prices, open(fn, 'wt'))

