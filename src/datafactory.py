from src.data import *
from src.abstractfactory import DataFactory

class DummyDataFactory(DataFactory):
    def concretegeneration(self, features):
        return DummyDataGrubber(features)


class StupidDataFactory(DataFactory):
    def concretegeneration(self, features):
        return StupidDataGrubber(features)


