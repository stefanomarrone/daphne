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
        factory = EngineFactory(configuration)
        # Image section
        imageEngine = factory.generateImage()
        imagefactory = FactoryGenerator.generate(imageEngine)
        imagegrabber = imagefactory().generate(configuration)
        imagegrabber.grub(configuration)
        retval = True
    except Exception:
        pass
    return retval


def datagrab(configuration):
    retval = False
    try:
        factory = EngineFactory(configuration)
        # Data section
        dataEngine = factory.generateData()
        datafactory = FactoryGenerator.generate(dataEngine)
        datagrabber = datafactory().generate(configuration)
        datagrabber.grub(configuration)
        retval = True
    except Exception:
        pass
    return retval


def grab_name(configurationname):
    image_retval = False
    data_retval = False
    try:
        configuration = Configuration(configurationname)
        # Image section
        if configuration.get('flag_image'):
            image_retval = imagegrab(configuration)
        else:
            image_retval = True
        # Data section
        if configuration.get('flag_data'):
            data_retval = datagrab(configuration)
        else:
            data_retval = True
    except Exception:
        pass
    return image_retval, data_retval