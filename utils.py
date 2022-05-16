#####################
# File: Utils.py
# Author(s): Pedro Loures Alzamora
# last update:  11/05/2022
####################

#DEFINES
DEPTH = 2
LOG_FILE = "log"

# external modules
from posixpath import split
from socket import timeout
import requests
import sys # read argv
from reppy.robots import Robots # read robots.txt
from bs4 import BeautifulSoup # parse html
import time
from url_normalize import url_normalize
import urllib3
import certifi
import ssl
import traceback
import logging


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
            new_dict[_key1] = _key1 
            _key2 = next(_iterator2) # check next addable key
        
        # if_4: if key1 has not yet reached key2 to check: go to next key1
        elif _key1 < _key2 :
            _key2 = next(_iterator2) 
        
        # if_5: if key2 is already in key 1: check next keys
        elif _key1 == _key2:
            new_dict[_key1] = _key1 # add key2
            _key1 = next(_iterator1)
            _key2 = next(_iterator2) # go to next key
        
    return new_dict

def process_url(const_url, base_url):
    _url_beta = const_url

    # url treatment policy -> bad way of goto, this is porqueira
    for _ in range(1):
        #skip conditions
        if not _url_beta:
            _url_beta = None
            continue
        if len(_url_beta) < 2:
            _url_beta = None
            continue
        if not isinstance(_url_beta, str):
            _url_beta = None
            continue
        if _url_beta == 'javascript:void(0)':
            _url_beta = None
            continue
        if _url_beta[0] == '#':
            _url_beta = None
            continue
        if '?' in _url_beta:
            _url_beta = None
            continue
        if _url_beta[1] == ':': # treat cases like C:/, D:/ 
            _url_beta = None
            continue
        # treatment
        if base_url[-1] == '/': # treat base url (only used in seed)
            while base_url[-1]=='/':
                base_url = base_url[:-1]        
        if _url_beta[0] == '/': # treat cases where url is a path
            _url_beta = base_url + _url_beta 
        
        # if _url_beta[:4] == 'http': # removes "http", "https", etc. from _url_beta
        #     _url_beta = _url_beta.split('/', maxsplit=2)[2]
        # if _url_beta[:4] == 'www.': # removes "www" from _url_beta 
        #     _url_beta = _url_beta[4:]
        # if _url_beta[-1] == '/': # removes / from end of url
        #     while _url_beta[-1]=='/':
        #         _url_beta = _url_beta[:-1]
    
    _treated_url = url_normalize(_url_beta)
    # if return_url:
    #     url = 'http://' + str(url)
    #     return url, url
    return _treated_url

# add urls from a page to queue
def add_url_to_queue(HTML_soup, HTML_url, url_queue, visited_url={}, _url_depth=2):
    _a_tags = HTML_soup.find_all('a')
    _new_url_queue = {}

    for _tag in _a_tags:
        
        #url treatment polycy
        _tag_url = process_url(_tag.get('href') , HTML_url)
        if not _tag_url: continue
        if _tag_url in visited_url: continue

        # profundity limit
        _url_path = _tag_url.split('/', maxsplit=2)
        _url_path = _url_path[-1].split('/')
        if len(_url_path) > _url_depth + 1:
            # print('NÃO PASSOU: ' + str((_url_path, _tag_url)))
            continue
        # print('PASSOU: ' + str(_url_path))

        # Enquewing policy
        _new_url_queue[_tag_url] = _tag_url
    return _merge_sorted_dicts(url_queue, _new_url_queue)

def expand_frontier(visited_url, url_queue, http=None, depth=DEPTH):
    if not http:
        http = urllib3.PoolManager(
            # _cert_reqs='CERT_REQUIRED',
            # _ca_certs=certifi.where()
        )    

    error_log = []

    url_refused = True
    _state = ['PAGE_REQUEST', 'MAKE_SOUP', 'ADD_TO_QUEUE']
    _iter_state = 0
    _visited_key = list(visited_url)[-1]
    #_url = "http://" + _visited_key
    _url = _visited_key
    try:
        _iter_state = 0
 #       print("[STATE: " + _state[_iter_state] + "]")
        _lap_time = time.time()
        _page_request = http.request(
                'GET',
                _url,
#                timeout=6.0
        )
        ftime = time.time() - _lap_time
        _iter_state = 1
 #       print("[STATE: " + _state[_iter_state] + "]")

        _soup = BeautifulSoup(_page_request.data, 'html.parser')
        visited_url[_visited_key] = len(str(_soup))
        _iter_state = 2
 #       print("[STATE: " + _state[_iter_state] + "]")
        
        url_queue = add_url_to_queue(_soup, _url, url_queue, visited_url, _url_depth=depth)
    except Exception as _exception: 
        url_refused = True
        _error_message = "[STATE: " + _state[_iter_state] + "] couldn't access: " + _url + "\n" + str(_exception)
        print(_error_message)
        with open(LOG_FILE, "a") as log_file:
            log_file.write(_error_message)
            log_file.write(traceback.format_exc())
        # print("[STATE: " + _state[_iter_state] + "] couldn't access: " + _url)
        # print(_expection)
        error_log.append(_error_message)
        ftime = time.time() - _lap_time
    return _url, url_queue, url_refused, ftime