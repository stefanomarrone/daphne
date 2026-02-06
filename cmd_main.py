import sys
import os
from src.configuration import Configuration
from src.concretefactory import FactoryGenerator
from src.abstractfactory import EngineFactory


# Configuration functions
def singleextractor(configurationname):
    retval = [configurationname]
    return retval


def folderextractor(foldername):
    retval = list(os.listdir(foldername))
    retval = list(filter(lambda x: x.endswith(".ini"), retval))
    return retval


def dumbextractor(dumbfile):
    return list()


modes = {
    'single': singleextractor,
    'folder': folderextractor
}


# single working function
def grab(configurationname):
    configuration = Configuration(configurationname)
    # Image section
    imageEngine = EngineFactory().generateImage(configuration)
    if imageEngine is not None:
        imagefactory = FactoryGenerator().generate(imageEngine)
        imagegrabber = imagefactory().generate(configuration)
        imagegrabber.grub(configuration)
    # Data section
    dataEngine = EngineFactory().generateData(configuration)
    if dataEngine is not None:
        datafactory = FactoryGenerator().generate(dataEngine)
        datagrabber = datafactory().concretegeneration(configuration)
        datagrabber.grub(configuration)


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
            grab(configurationname)
    else:
        errormessage()