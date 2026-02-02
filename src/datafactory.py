from src.data import *
from src.abstractfactory import DataFactory

class DummyDataFactory(DataFactory):
    def concretegeneration(self, features):
        return DummyDataGrubber(features)


class OPWDataFactory(DataFactory):
    def concretegeneration(self, configuration):
        return OPWDataGrabber(configuration)
