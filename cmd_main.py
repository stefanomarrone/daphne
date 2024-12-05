import sys
import os
from src.core import grab_name

# Configuration functions
def singleextractor(configurationname):
    retval = [configurationname]
    return retval


def folderextractor(foldername):
    retval = list(os.listdir(foldername))
    retval = list(filter(lambda x: x.endswith(".ini"), retval))
    retval = list(map(lambda x: foldername + x, retval))
    return retval


def dumbextractor(dumbfile):
    return list()


modes = {
    'single': singleextractor,
    'folder': folderextractor
}

def errormessage():
    print('There is an error in the command line! There are two arguments.')
    print('The first argument to use is the mode: "single" and "folder".')
    print('In case of "single" mode, the second argument is the configuration file.')
    print('In case of "folder" mode, the second argument is a folder containing different configuration files.')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        mode = sys.argv[1]
        nameextractor = modes.get(mode, dumbextractor)
        configurationnames = nameextractor(sys.argv[2])
        for configurationname in configurationnames:
            grab_name(configurationname)
    else:
        errormessage()


#todo: testing last changes with the fastapi approach
#todo: integrate the simulator
#todo: to implement the NDVI data provider
#todo: to implement the data provider
#todo: improve deployability