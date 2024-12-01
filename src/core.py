from src.abstractfactory import EngineFactory
from src.concretefactory import FactoryGenerator
from src.configuration import Configuration
import tempfile

def grab(configuration):
    retval = (False, False)
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        f.write(configuration)
        f.flush()
        retval = grab_name(tmp.name)
    return retval

def imagegrab(configuration):
    retval = False
    try:
        # Image section
        imageEngine = EngineFactory.generateImage(configuration)
        imagefactory = FactoryGenerator.generate(imageEngine)
        imagegrabber = imagefactory().generate(configuration)
        imagegrabber.grab()
        retval = True
    except Exception as e:
        print(e)
    return retval

def datagrab(configuration):
    retval = False
    try:
        # Data section
        dataEngine = EngineFactory.generateData(configuration)
        datafactory = FactoryGenerator.generate(dataEngine)
        datagrabber = datafactory().generate(configuration)
        datagrabber.grab()
        retval = True
    except Exception as e:
        print(e)
    return retval

def grab_name(configurationname):
    image_retval = False
    data_retval = False
    try:
        configuration = Configuration(configurationname)
        # Image section
        image_retval = imagegrab(configuration)
        # Data section
        data_retval = datagrab(configuration)
    except Exception:
        pass
    return image_retval, data_retval