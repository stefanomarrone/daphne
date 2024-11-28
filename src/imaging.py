from src.catalog.imagecatalog import ImageCatalog

class ImageGrabber():
    def __init__(self, features):
        pass

    def grab(self):
        pass

class DummyImageGrabber(ImageGrabber):
    def grab(self):
        print("This is a test. And this is the DummyImageGrubber")

class StupidImageGrabber(ImageGrabber):
    def grab(self):
        print("This is a test. And this is the StupidImageGrubber")
