from src.imagefactory import *
from src.datafactory import *

class FactoryGenerator():

    def generate(self, factoryname):
        map = {
            'OPWDataFactory': OPWDataFactory,
            'GeeImageFactory': GeeImageFactory,
            'SkifyImageFactory': SkifyImageFactory
        }
        return map[factoryname]

