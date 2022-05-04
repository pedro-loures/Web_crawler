#1 TODO Get arguments from command line
#2 TODO Implement good practices
#3 TODO Reach seed
#4 TODO Read and robots.txt
#5 TODO Collect seed
#6 TODO Create heap from seed anchor text
#7 TODO implement multithreading

# external modules
import sys 

# internal modules
import utils

if __name__ == "__main__":
    argv = sys.argv

    # Assert Usage
    assert len(argv) > 5, "USAGE: python3 main.py -s <SEEDS> -n <LIMIT> [-d]"
    
    # Get arguments
    print(get_opt(argv))
    
    # 

    