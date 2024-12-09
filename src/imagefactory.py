from src.imaging import *
from src.abstractfactory import ImageFactory
from src.landsat import LandsatImageGrubber
from src.modis import ModisImageGrabber


class Landsat09ImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return LandsatImageGrubber(configuration, "Landsat09")

class Landsat08ImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return LandsatImageGrubber(configuration, "Landsat08")

class ModisImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return ModisImageGrabber(configuration)

class DummyImageFactory(ImageFactory):
    def concretegeneration(self, features):
        return DummyImageGrabber(features)

class StupidImageFactory(ImageFactory):
    def concretegeneration(self, features):
        return StupidImageGrabber(features)


