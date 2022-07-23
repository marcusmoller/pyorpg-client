import time
import json
import os


def log(msg):
    ''' Prints @msg to the terminal with a timestamp '''
    localTime = time.localtime(time.time())
    stringTime = str(localTime[3]) + ":" + str(localTime[4]) + ":" + str(localTime[5])

    print(stringTime + ": " + msg)


def decodeJSON(data):
    '''Decodes JSON from a @data'''
    result = json.loads(data)

    return result

def countFiles(folder):
    """ Counts the number of files in a directory """
    count = 0
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, f)):
            count += 1

    return count
