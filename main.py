#-0 OK assert usage
#-1 OK Get arguments from command line
#-2 OK Reach seed
#-3 OK Collect seed
#-4 OK Implement good practices
#-5 OK Read and respect robots.txt
#-6 OK Create heap from seed anchor text
#-7 OK parse heap
#-8 TODO save corpus
#-9 TODO implement multithreading
#10 TODO Create Debug mode



# >>>> 2.1 TODO: fix 'Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER.' 
# 2.2 TODO: read sitemap

# 4.1 OK: implement a default of at least 100ms between consecutive request to the same website
# 4.2 OK: abide by the Robots eclusion standart

# 6.1 TODO: implement selection policy (only follow links to html pages)
# 6.1 OK: update url processing using url_normalize
# 6.3 OK: implement profundity limit
# 6.4 OK: implement normalization and enqueing policy
# 6.5 TODO: implement better way to dequeue
# 6.x TODO FUTURE: implement revisitation policy
# 6.x TODO FUTURE: implement graph


# 7.1 TODO Check for duplicates

# 8.1 TODO: save raw HTML content using WARC format (1000 webpages per file)
# 8.2 TODO: compress with gzip


# CONVENTIONS:
#   fun() -> Uses action
#   var   -> Uses states


PATH_TO_CORPUS = "C:\\Users\\PLour\\OneDrive - Universidade Federal de Minas Gerais\\01_Estudos\\Faculdade\\RI\\Crawler\\Corpus"

# external modules
import sys 
import requests
from reppy.robots import Robots # ler robots.txt
from bs4 import BeautifulSoup # parse html

# internal modules
import utils as ut # funções pessoais

def main(argv):
    

    # 0, 1 Assert Usage and get options
    seed_url, page_limit, is_debug = ut.get_opt(argv)
 
    # 3
    url = 'http://portalms.saude.gov.br/'
    page = requests.get(url, auth=('user', 'pass'))
    
    #
    soup = BeautifulSoup(page.content, 'html.parser')
    print(len(ut.add_url_to_queue(soup, url)))
    
    # # This utility uses `requests` to fetch the content
    # robots = Robots.fetch('http://portalms.saude.gov.br/robots.txt')
    # robots.allowed('http://portalms.saude.gov.br/', 'my-user-agent')


    # # Get the rules for a specific agent
    # agent = robots.agent('my-user-agent')
    # agent.allowed('http://portalms.saude.gov.br/')

     

    
    


if __name__ == "__main__":
    argv = sys.argv
    main(argv)