from src.imagefactory import *
from src.datafactory import *

class FactoryGenerator():

    def generate(self, factoryname):
        map = {
            'OPWDataFactory': OPWDataFactory,
            'ModisImageFactory': ModisImageFactory,
            'Landsat09ImageFactory': Landsat09ImageFactory,
            'SkifyImageFactory': SkifyImageFactory
        }
        return map[factoryname]

