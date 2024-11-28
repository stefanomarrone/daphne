from src.imaging import *
from src.data import *


class GrabberFactory():
    def generate(self, configuration):
        features = self.getfeatures(configuration)
        return self.concretegeneration(features)


class ImageFactory(GrabberFactory):
    def getfeatures(self, configuration):
        featurenames = ['fromdate', 'todate', 'longitude', 'country_name', 'latitude', 'area', 'imageresolution', 'format', 'imagetimeinterval']
        features = configuration.extract(featurenames)
        return features

class DataFactory(GrabberFactory):
    def getfeatures(self, configuration):
        featurenames = ['data', 'datatimeinterval']
        features = configuration.extract(featurenames)
        return features


class EngineFactory:

    def generateImage(configuration):
        re = 'imageRE'
        fnames = ['fromdate', 'todate', 'longitude', 'latitude', 'area', 'imageresolution', 'format', 'imagetimeinterval']
        return EngineFactory.generate(configuration, re, fnames)


    def generateData(configuration):
        re = 'dataRE'
        fnames = ['fromdate', 'todate', 'longitude', 'latitude', 'area', 'imageresolution', 'format', 'imagetimeinterval']
        return EngineFactory.generate(configuration, re, fnames)


    def generate(configuration, re, fnames):
        engine = configuration.get(re)
        features = configuration.extract(fnames)
        match = engine.match(features)
        return match