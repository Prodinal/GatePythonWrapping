import sys
import os
from subprocess import Popen, PIPE, check_output, call


if __name__ == '__main__':
    sentence = sys.argv[1]
    file_name = 'temp.txt'

    dirname = os.path.dirname(__file__)
    quntoken_path = os.path.join(dirname, './quntoken')
    with open(file_name, 'w+') as f:
        f.write(sentence)

    # p = Popen(['quntoken', file_name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    # print(p.returncode)

    analysis = check_output([quntoken_path + ' ' + file_name], shell=True,
                            universal_newlines=True)

    print(analysis)

    os.remove(file_name)
