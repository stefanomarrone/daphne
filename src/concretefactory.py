from src.imagefactory import *
from src.datafactory import *

class FactoryGenerator():

    def generate(self, factoryname):
        map = {
            'DummyDataFactory': DummyDataFactory,
            'DummyImageFactory': DummyImageFactory,
            'StupidDataFactory': StupidDataFactory,
            'StupidImageFactory': StupidImageFactory,
            'OPWDataFactory': OPWDataFactory,
            'ModisImageFactory': ModisImageFactory,
            'Landsat09ImageFactory': Landsat09ImageFactory
        }
        return map[factoryname]

