from imaging import *
from abstractfactory import ImageFactory

class DummyImageFactory(ImageFactory):
    def concretegeneration(self, features):
        return DummyImageGrubber(features)


class StupidImageFactory(ImageFactory):
    def concretegeneration(self, features):
        return StupidImageGrubber(features)


