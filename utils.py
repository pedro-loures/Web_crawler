#####################
# File: Utils.py
# Author(s): Pedro Loures Alzamora
# last update:  11/05/2022
####################

# external modules
import sys # read argv
from reppy.robots import Robots # read robots.txt
from bs4 import BeautifulSoup # parse html

# Internal modules




# Index
#   # Internal functions
#       def _assert_usage_len(argv): # assert argv is of correct len              
#       def _assert_usage_arguments(argument): # assert argv has the right arguments
# 
#   # External functions
#       def get_opt(argv): # assert usage and return the correct arguments of the argv
#

def _assert_usage_len(argv):
    assert len(argv) > 5, "USAGE: python3 main.py -s <SEEDS> -n <LIMIT> [-d]"

def _assert_usage_arguments(argument):
    if len(argument) == 1:
        assert argument[0] == '-d', "USAGE: python3 main.py -s <SEEDS> -n <LIMIT> [-d]"
    else:
        assert argument[0] in ['-s', '-n'], "USAGE: python3 main.py -s <SEEDS> -n <LIMIT> [-d]"

# assert usage and return the correct arguments of the argv
def get_opt(argv):
    # Return
    seed_url = ''
    page_limit = ''
    is_debug = False
    
    # Assert correct number of argument
    _assert_usage_len(argv)
    

    # separate argument in list of list
    _options = []
    _i = 0
    while _i < len(argv[:-1]):

        _i+=1
        _options.append([argv[_i]])
        if argv[_i][0] == '-' and _i + 1 < len(argv):
            _options[-1].append(argv[_i+1])
            _i+=1

    # Fill return values and assert correct input argument usage
    for _option in _options:
        _assert_usage_arguments(_option)
        if _option[0] == '-d':
            is_debug = True 
        elif _option[0] == '-n':
            page_limit = _option[1]
        elif _option[0] == '-s':
            seed_url = _option[1]

    return seed_url, page_limit, is_debug


# allow to merge two ordered dicts
def _merge_sorted_dicts(sorted_dict1, dict2):
    new_dict = {}

#    print('MERGE FUN')
    _sorted_keys1 = list(sorted_dict1.keys()) + ['STOP_KEY']
    _sorted_keys2 = list(sorted(dict2.keys())) + ['STOP_KEY']
    _max_size_queue = len(_sorted_keys1) + len(_sorted_keys2)

    _iterator1 = iter(_sorted_keys1)
    _iterator2 = iter(_sorted_keys2)

    _key1 = next(_iterator1)
    _key2 = next(_iterator2)
    for _ in range(_max_size_queue):
        # if_2: if  we have checked all non previous keys: add rest of key2
        if _key1 == 'STOP_KEY':
            while _key2 != 'STOP_KEY':
                new_dict[_key2] = _key2 # may cause redundancy with if_1
                _key2 = next(_iterator2)
            break
        
        # if_1: if we have checked all addable keys: add rest of key1
        elif _key2 == 'STOP_KEY':
            while _key1 != 'STOP_KEY':
                new_dict[_key1] = _key1 # may cause redundancy with if_1
                _key1 = next(_iterator1)
            break

        # if_3: if key2 not present in key1: add key2 to sorted dict
        elif _key1 > _key2:
            new_dict[_key2] = _key2 # add key2
            _key2 = next(_iterator2) # check next addable key
            new_dict[_key1] = _key1 
        
        # if_4: if key1 has not yet reached key2 to check: go to next key1
        elif _key1 < _key2 :
            _key2 = next(_iterator2) 
        
        # if_5: if key2 is already in key 1: check next keys
        elif _key1 == _key2:
            _key1 = next(_iterator1)
            _key2 = next(_iterator2) # go to next key
            new_dict[_key1] = _key1 # add key2
        
    return new_dict

# Aplica o tratamento de string para o url
def process_url(const_url):
    url = const_url
    if url[-1] == '/':
        url = url[:-1]

    domain = url
    url = 'http://' + url
    return domain, url

# add urls from a page to queue
def add_url_to_queue(HTML_soup, HTML_url, url_queue, _url_depth=2):
    _a_tags = HTML_soup.find_all('a')
    _new_url_queue = {}

    for _tag in _a_tags:
        # url treatment policy
        _tag_url = _tag.get('href')
        if not isinstance(_tag_url, str):
            continue
        if _tag_url == 'javascript:void(0)':
            continue
        if _tag_url[0] == '#':
            continue
        if _tag_url[0] == '/': 
            _tag_url = HTML_url + _tag_url 
        if _tag_url[:4] == 'http':
            _tag_url = _tag_url.split('/', maxsplit=2)[2]
        if _tag_url[:4] == 'www.':
            _tag_url = _tag_url[4:]
        if _tag_url[-1] == '/':
            _tag_url = _tag_url[:-1]
        
        # profundity limit
        _url_path = _tag_url.split('/')
        if len(_url_path) > _url_depth:
            continue

        # Enquewing policy
        _new_url_queue[_tag_url] = _tag_url
    return _merge_sorted_dicts(url_queue, _new_url_queue)


# Check robots.txt to see if allowed in page and crawl delay policy
def check_robots(url, robots=None, delay=0.1):
    _url ='http://'+ url
    _url_prefix ='http://'+ url.split('/', maxsplit=1)[0]
    _path_to_robots = _url_prefix + '/'+ Robots.robots_url(_url)


    if not robots:
        try:
            robots = Robots.fetch(_path_to_robots)
            robots_allowed = robots.allowed(_url, 'my-user-agent')
            # print("[NO ROBOTS] - OK!", _path_to_robots)
            return robots_allowed, robots
        except:
            # print("[NO ROBOTS] - couldn't access robots: ", _path_to_robots)
            return True, None
    try:
        robots_allowed = robots.allowed(_url, 'my-user-agent')
        robots_delay =  robots.agent('my-user-agent').delay
        # print("[WITH ROBOTS] - OK!", _path_to_robots)
        return robots_allowed, robots_delay
    except:
        # print("[WITH ROBOTS] - couldn't access URL: ", _path_to_robots)
        return True, delay




# save html soup produced by beatiful soup
# def store_soup(soup, path_to_fridge):
#     with open('teste.txt', 'w') as f:
#         f.write(str(r.text))
