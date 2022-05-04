import sys

def get_opt(argv):
    opt = []
    i = 0
    while i < len(argv[:-1]):

        i+=1
        opt.append([argv[i]])
        if argv[i][0] == '-' and i + 1 < len(argv):
            print(opt[-1])
            opt[-1].append(argv[i+1])
            i+=1

    return opt

