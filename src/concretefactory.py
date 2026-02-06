from src.imagefactory import *
from src.datafactory import *

class FactoryGenerator():

    def generate(factoryname):
        map = {
            'OPWDataFactory': OPWDataFactory,
            'GeeImageFactory': GeeImageFactory,
            'SkifyImageFactory': SkifyImageFactory
        }
        return map[factoryname]

