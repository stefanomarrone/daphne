from data import *
from abstractfactory import DataFactory

class DummyDataFactory(DataFactory):
    def concretegeneration(self, features):
        return DummyDataGrubber(features)


class StupidDataFactory(DataFactory):
    def concretegeneration(self, features):
        return StupidDataGrubber(features)


