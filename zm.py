#!/usr/bin/python3

import os
import sys
import re
import pickle
import subprocess

if __name__ == "__main__":

    db = {}

    CC = os.getenv("CC") and os.getenv("CC") or "gcc"

    if os.path.isfile(".zm.pickle"):
        db = pickle.load(open(".zm.pickle", "rb"))
    elif len(sys.argv) == 1:
        print("zero make - make done easy")
        print("usage=zm.py [options] and CC build commands")
        print("--clean\tremove object files")
        print("--rebuild\trebuild everything")
        print("--purge\tremove all stored data")
        print("--make\tgenerate template makefile")
        print("--list\tlist template makefile")
        sys.exit(0)
        
    if len(sys.argv) == 1:
        for k in db:
            (cfile, obj) = k
            if not os.path.isfile(obj) or not os.path.isfile(cfile) or os.stat(cfile).st_mtime > os.stat(obj).st_mtime:
                subprocess.run(CC + " " + " ".join(db[k]), shell=True)

    if len(sys.argv) > 1:
        if sys.argv[1] == '--clean':
            for k in db:
                try:
                    os.remove(k[1])
                    print("rm " + k[1])
                except: 
                    pass

        elif sys.argv[1] == '--purge':
            db = {}
            os.remove(".zm.pickle")

        elif sys.argv[1] == '--list':
            for k in db:
                print("CC " + " ".join(db[k]))                
            
        elif sys.argv[1] == '--rebuild':
            pass
        else:
            l = list(filter(lambda x: x.endswith('.c') and os.path.isfile(x), sys.argv[1:]))

            # found c-file argslist            
            if len(l):
                db[(l[0],l[0].replace(".c", ".o"))] = sys.argv[1:]

    if db:
        pickle.dump(db, open(".zm.pickle", "wb"))
