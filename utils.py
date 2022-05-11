import sys

def _assert_usage_len(argv):
    assert len(argv) > 5, "USAGE: python3 main.py -s <SEEDS> -n <LIMIT> [-d]"

def _assert_usage_arguments(argument):
    if len(argument) == 1:
        assert argument[0] == '-d', "USAGE: python3 main.py -s <SEEDS> -n <LIMIT> [-d]"
    else:
        assert argument[0] in ['-s', '-n'], "USAGE: python3 main.py -s <SEEDS> -n <LIMIT> [-d]"

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

