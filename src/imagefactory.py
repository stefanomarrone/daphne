from src.imaging import *
from src.abstractfactory import ImageFactory
from src.landsat import Landsat09ImageGrubber
from src.modis import ModisImageGrabber


class Landsat09ImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return Landsat09ImageGrubber(configuration)

class ModisImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return ModisImageGrabber(configuration)

class DummyImageFactory(ImageFactory):
    def concretegeneration(self, features):
        return DummyImageGrabber(features)

class StupidImageFactory(ImageFactory):
    def concretegeneration(self, features):
        return StupidImageGrabber(features)


