from src.imaging import *
from src.data import *


class GrabberFactory():

    def generate(self, configuration):
        features = self.getfeatures(configuration)
        return self.concretegeneration(features)


class ImageFactory(GrabberFactory):
    def getfeatures(self, configuration):
        featurenames = ['fromdate', 'todate', 'longitude', 'latitude', 'countryname', 'area', 'imageresolution', 'format',
                        'imagetimeinterval']
        features = configuration.extract(featurenames)
        return features


class DataFactory(GrabberFactory):
    def getfeatures(self, configuration):
        featurenames = ['data', 'datatimeinterval']
        features = configuration.extract(featurenames)
        return features


class EngineFactory:

    def __init__(self, configuration):
        self.configuration = configuration

    def generateImage(self):
        re = 'imageRE'
        fnames = ['fromdate', 'todate', 'longitude', 'latitude', 'countryname', 'area', 'imageresolution', 'format', 'imagetimeinterval']
        try:
            self.configuration.board[re]
        except Exception:
            return None
        return EngineFactory.generate(self, re, fnames)

    def generateData(self):
        re = 'dataRE'
        fnames = ['fromdate', 'todate', 'longitude', 'latitude', 'countryname', 'area', 'imageresolution', 'format',
                  'imagetimeinterval']
        try:
            self.configuration.board[re]
        except Exception:
            return None
        return EngineFactory.generate(self, re, fnames)

    def generate(self, re, fnames):
        engine = self.configuration.get(re)
        features = self.configuration.extract(fnames)
        match = engine.match(features)
        return match
