from src.data import *
from src.abstractfactory import DataFactory

class DummyDataFactory(DataFactory):
    def concretegeneration(self, features):
        return DummyDataGrubber(features)


class StupidDataFactory(DataFactory):
    def concretegeneration(self, features):
        return StupidDataGrubber(features)


class OPWDataFactory(DataFactory):
    def concretegeneration(self, configuration):
        return OPWDataGrabber(configuration)

class OpenMeteoPyFactory(DataFactory):
    def concretegeneration(self, configuration):
        return OpenMeteoPyGrabber(configuration)

class VisualCrossingFactory(DataFactory):
    def concretegeneration(self, configuration):
        return VisualCrossingGrabber(configuration)