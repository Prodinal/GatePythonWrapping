import sys
import os
import pickle
from LocalSpacyHu.HunTag3 import transmodel


# https://stackoverflow.com/questions/2121874/python-pickling-after-changing-a-modules-directory
def main():
    fileName = '/home/mrengineer/School/DipTerv/GatePythonWrapping/LocalSpacyHu/HunTag3/models/maxNP-szeged-hfst-model/maxNP-szeged-hfst.transmodel'
    sys.modules['transmodel'] = transmodel
    with open(fileName, 'rb') as f:
        myObject = pickle.load(f)
    sys.modules.pop('transmodel', None)
    os.remove(fileName)
    with open(fileName, 'wb') as f:
        pickle.dump(myObject, f)

    print('Done c:')

if __name__ == '__main__':
    main()
