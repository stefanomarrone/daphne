from src.imaging import *
from src.abstractfactory import ImageFactory

class Landsat09ImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return Landsat09ImageGrubber(configuration)

class ModisImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return ModisImageGrubber(configuration)

class SkifyImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return SkifyImageGrubber(configuration)


