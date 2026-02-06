from src.imaging import *
from src.abstractfactory import ImageFactory
from call4API.Image.GeeAPI import *

class GeeImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        gee_api = GeeAPI(strategies={
            "MODIS": ModisStrategy(),
            "LANDSAT09": Landsat09Strategy(),
        })
        return GeeImageGrubber(configuration, gee_api)

class SkifyImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return SkifyImageGrubber(configuration)


class NoImageFactory(ImageFactory):
    def concretegeneration(self, configuration):
        return NoImageGrubber(configuration)
