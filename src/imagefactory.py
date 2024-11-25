from src.imaging import *
from src.abstractfactory import ImageFactory

class Landsat09ImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return Landsat09ImageGrubber(configuration)

class ModisImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return ModisImageGrubber(configuration)

class DummyImageFactory(ImageFactory):
    def concretegeneration(self, features):
        return DummyImageGrubber(features)

class StupidImageFactory(ImageFactory):
    def concretegeneration(self, features):
        return StupidImageGrubber(features)


