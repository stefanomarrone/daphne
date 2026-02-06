from src.imagefactory import *
from src.datafactory import *

class FactoryGenerator():

    def generate(factoryname):
        map = {
            'NoData': NoDataFactory,
            'NoImage': NoImageFactory,
            'OPWDataFactory': OPWDataFactory,
            'GeeImageFactory': GeeImageFactory,
            'SkifyImageFactory': SkifyImageFactory
        }
        return map[factoryname]

