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

    def generateImage(self, configuration):
        re = 'imageRE'
        fnames = ['fromdate', 'todate', 'longitude', 'latitude', 'countryname', 'area', 'imageresolution', 'format',
                  'imagetimeinterval']
        try:
            configuration.board[re]
        except Exception:
            return None
        return EngineFactory.generate(self,configuration, re, fnames)

    def generateData(self, configuration):
        re = 'dataRE'
        fnames = ['fromdate', 'todate', 'longitude', 'latitude', 'countryname', 'area', 'imageresolution', 'format',
                  'imagetimeinterval']
        try:
            configuration.board[re]
        except Exception:
            return None
        return EngineFactory.generate(self, configuration, re, fnames)

    def generate(self, configuration, re, fnames):
        engine = configuration.get(re)
        features = configuration.extract(fnames)
        match = engine.match(features)
        return match
