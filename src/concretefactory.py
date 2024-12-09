from src.imagefactory import *
from src.datafactory import *

class FactoryGenerator():
    map = {
        'DummyDataFactory': DummyDataFactory,
        'DummyImageFactory': DummyImageFactory,
        'StupidDataFactory': StupidDataFactory,
        'StupidImageFactory': StupidImageFactory,
        'OPWDataFactory': OPWDataFactory,
        'ModisImageFactory': ModisImageFactory,
        'Landsat09ImageFactory': Landsat09ImageFactory,
        'Landsat08ImageFactory': Landsat08ImageFactory
    }

    def generate(factoryname):
        return FactoryGenerator.map[factoryname]

