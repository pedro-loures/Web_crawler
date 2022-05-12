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

def _merge_ordered_dicts(dict1, dict2):
    return

# add urls from a page to queue
def add_url_to_queue(HTML_soup, HTML_url, url_queue, _url_depth=5):
    _a_tags = HTML_soup.find_all('a')
    _new_url_queue = {}
    for _tag in _a_tags:
        # url treatment policy
        _tag_url = _tag.get('href')
        if not isinstance(_tag_url, str):
            continue
        if _tag_url[0] == '#':
            continue
        if _tag_url[0] == '/': 
            _tag_url = HTML_url + _tag_url[1:]   
        if _tag_url[:4] == 'http':
            _tag_url = _tag_url.split('/', maxsplit=2)[2]
        if _tag_url[:4] == 'www.':
            _tag_url = _tag_url[4:]
        
        # profundity limit
        _url_path = _tag_url.split('/')
        if len(_url_path) > _url_depth:
#            print(_tag_url)
#            print(_url_path)
            continue


#        print(_tag_url)
        # Enquewing policy
        _new_url_queue[_tag_url] = _tag_url
    return _new_url_queue

def check_robots(url):
    return

# save html soup produced by beatiful soup
# def store_soup(soup, path_to_fridge):
#     with open('teste.txt', 'w') as f:
#         f.write(str(r.text))
