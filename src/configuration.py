from configparser import ConfigParser
from src.engine import RuleEngine
import configparser

from src.metaclasses import Singleton


class Configuration(metaclass=Singleton):
    def __init__(self, inifilename):
        self.board = dict()
        self.load(inifilename)

    def get(self, key):
        return self.board[key]

    def put(self, key, value):
        self.board[key] = value

    @staticmethod
    def tolist(value):
        retval = value.split(',')
        return retval

    def loadSection(self,reader,s):
        temp = dict()
        options = []
        try:
            options = reader.options(s)
        except configparser.NoSectionError as nse:
            temp[s] = ['*']
        for o in options:
            try:
                value = reader[s][o]
                temp[s] = self.tolist(value)
            except:
                print("exception on %s!" % o)
        return temp

    def loadIndices(self, reader):
        temp = dict()
        options = reader.options("indices")
        for o in options:
            value = reader["indices"][o]
            temp[o] = self.tolist(value)
        retval = dict()
        retval["indices"] = temp
        return retval

    def loadDetails(self,reader):
        temp = dict()
        options = reader.options("details")
        for o in options:
            value = reader["details"][o]
            temp[o] = self.tolist(value)
        retval = dict()
        retval["details"] = temp
        return retval

    def extract(self, keylist):
        retval = dict()
        for key in keylist:
            retval[key] = self.board[key]
        return retval


    def load(self, inifile):
        reader = ConfigParser()
        reader.read(inifile)
        #MAIN
        if reader.has_section('main'):
            temp = reader['main'].get('outfolder', '')
            self.put('outfolder', temp)
            kb = reader['main'].get('datakb')
            if kb is not None:
                dg = reader['main'].get('defaultdatafactory', '')
                engine = RuleEngine(kb,dg)
                self.put('dataRE', engine)
            kb = reader['main'].get('imagekb')
            if kb is not None:
                dg = reader['main'].get('defaultimagefactory', 'GeeImageFactory')
                engine = RuleEngine(kb,dg)
                self.put('imageRE', engine)
            temp = reader['main'].get('fromdate', '2023-06-01 12:00:00')
            self.put('fromdate', temp)
            temp = reader['main'].get('todate', '2024-05-01 12:00:00')
            self.put('todate', temp)
        #IMAGE
        if reader.has_section('image'):
            temp = reader['image'].get('longitude', '18.105889')
            self.put('longitude', float(temp))
            temp = reader['image'].get('latitude', '-28.038970')
            self.put('latitude', float(temp))
            temp = reader['image'].get('area', '100')
            self.put('area', float(temp))
            temp = reader['image'].get('countryname', '')
            self.put('countryname', temp)
            temp = reader['image'].get('imageresolution', '250')
            self.put('imageresolution', int(temp))
            temp = reader['image'].get('format', 'jpg')
            self.put('format', temp)
            temp = reader['image'].get('imagetimeinterval', '10')
            self.put('imagetimeinterval', float(temp))
            temp = reader['image'].get('resolutions', [])
            temp = self.tolist(temp)
            self.put('resolutions', temp)
            temp = reader['image'].get('productTypes', [])
            temp = self.tolist(temp)
            self.put('productTypes', temp)
            temp = reader['image'].get('providers', [])
            temp = self.tolist(temp)
            self.put('providers', temp)
            temp = reader['image'].get('openData', 'True')
            self.put('openData', temp)
            temp = reader['image'].get('maxCloudCoveragePercent', 100)
            self.put('maxCloudCoveragePercent', int(temp))
        #SKYFI
        if reader.has_section('skyfi'):
            temp = reader['skyfi'].get('catalogfolder', None)
            self.put('catalogfolder', temp)
            temp = reader['skyfi'].get('orderrequestfolder', None)
            self.put('orderrequestfolder', temp)
            temp = reader['skyfi'].get('orderresponsefolder', None)
            self.put('orderresponsefolder', temp)
            temp = reader['skyfi'].get('downloadimagefolder', None)
            self.put('downloadimagefolder', temp)
            temp = reader['skyfi'].get('deliverabletype', 'image')
            self.put('deliverabletype', str(temp))


        #DATA
        if reader.has_section('data'):
            datalist = self.tolist(reader['data']['data'])
            self.put('data', datalist)
            temp = reader['data'].get('datatimeinterval', '10')
            self.put('datatimeinterval', float(temp))

