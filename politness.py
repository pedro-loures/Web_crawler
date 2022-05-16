#####################
# File: Utils.py
# Author(s): Pedro Loures Alzamora
# last update:  12/05/2022
####################

# External Modules
from reppy.robots import Robots # read robots.txt
import time



# Check robots.txt to see if allowed in page and crawl delay policy
def _check_robots(url, robots=None, delay=0.1):
    _url = url
    _url_prefix = url.split('/', maxsplit=1)[0]
    _path_to_robots = Robots.robots_url(_url)


    if not robots:
        try:
            robots = Robots.fetch(_path_to_robots)
            robots_allowed = robots.allowed(_url, 'my-user-agent')
#            print("[NO ROBOTS] - OK!", _url_prefix,', ', _path_to_robots)
            return robots_allowed, robots
        except:
#            print("[NO ROBOTS] - couldn't access robots: ", _url_prefix,', ', _path_to_robots)
            return True, None
    try:
        robots_allowed = robots.allowed(_url, 'my-user-agent')
        robots_delay =  robots.agent('my-user-agent').delay
#       print("[WITH ROBOTS] - OK!", _url_prefix,', ', _path_to_robots)
        return robots_allowed, robots_delay
    except:
#       print("[WITH ROBOTS] - couldn't access URL: ", _url_prefix,', ', _path_to_robots)
        return True, delay

# quick function to implement correct delay
def sleep_delay(delay=None):
    if not delay:
        time.sleep(0.1)
    else:
        time.sleep(delay)

# impementation of good plocies regarding robots.txt
def obey_robots(url, _url_prefix, _previous_url_prefix, robots):
    _lap_time = time.time()
    
    if _url_prefix != _previous_url_prefix:
        # print("awake")
        allowed, robots = _check_robots(url)
    else:
        # assert robots, '[NO ROBOTS ON A VISITED PAGE]'
        if not robots:
            print('[NO ROBOTS ON A VISITED PAGE]')
            allowed, robots = _check_robots(url)
            allowed, delay = _check_robots(url,robots)
        else:
            allowed, delay = _check_robots(url, robots)
        # print("sleep")
        sleep_delay(delay)
    
    
    # check if allowed
    should_continue = False
    if not allowed:
        print('not allowed in: ' + url)
        should_continue = True
    robots_time = time.time() - _lap_time
    
    return should_continue, robots_time, robots
