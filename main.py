#0 OK assert usage
#1 OK Get arguments from command line
#2 TODO Implement good practices
#3 TODO Reach seed
#4 TODO Read and robots.txt
#5 TODO Collect seed
#6 TODO Create heap from seed anchor text
#7 TODO implement multithreading


# CONVENTIONS:
#   fun() -> Uses action
#   var   -> Uses states


PATH_TO_CORPUS = "C:\\Users\\PLour\\OneDrive - Universidade Federal de Minas Gerais\\01_Estudos\\Faculdade\\RI\\Crawler\\Corpus"

# external modules
import sys 
import requests

# internal modules
import utils as ut

if __name__ == "__main__":
    argv = sys.argv

    # 0, 1 Assert Usage and get options
    seed_url, page_limit, is_debug = ut.get_opt(argv)
 
    # 3
    r = requests.get('http://portalms.saude.gov.br/', auth=('user', 'pass'))
    print(r.status_code)

     

    