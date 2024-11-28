from src.catalog.image_catalog import image_catalog

class ImageGrabber():
    def __init__(self, features):
        pass
        self.features = features
        self.catalog = image_catalog()

class DummyImageGrubber(ImageGrabber):
    def grub(self):
        print("This is a test. And this is the DummyImageGrubber")

class StupidImageGrubber(ImageGrabber):
    def grub(self):
        print("This is a test. And this is the StupidImageGrubber")
