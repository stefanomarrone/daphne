from src.abstractfactory import EngineFactory
from src.concretefactory import FactoryGenerator
from src.configuration import Configuration
import tempfile


def grab(configuration):
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        f.write(configuration)
        f.flush()
        grab_name(tmp.name)


def grab_name(configurationname):
    configuration = Configuration(configurationname)
    # Image section
    imageEngine = EngineFactory.generateImage(configuration)
    imagefactory = FactoryGenerator.generate(imageEngine)
    imagegrabber = imagefactory().generate(configuration)
    imagegrabber.grub()
    # Data section
    dataEngine = EngineFactory.generateData(configuration)
    datafactory = FactoryGenerator.generate(dataEngine)
    datagrabber = datafactory().generate(configuration)
    datagrabber.grub()
