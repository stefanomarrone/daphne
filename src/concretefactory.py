from imagefactory import *
from datafactory import *

class FactoryGenerator():

    def generate(factoryname):
        map = {
            'DummyDataFactory': DummyDataFactory,
            'DummyImageFactory': DummyImageFactory,
            'StupidDataFactory': StupidDataFactory,
            'StupidImageFactory': StupidImageFactory
        }
        return map[factoryname]

