from src.data import *
from src.abstractfactory import DataFactory

class OPWDataFactory(DataFactory):
    def concretegeneration(self, configuration):
        return OPWDataGrabber(configuration)

class NoDataFactory(DataFactory):
    def concretegeneration(self, configuration):
        return NoDataGrubber(configuration)
