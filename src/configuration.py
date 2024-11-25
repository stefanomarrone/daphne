import tempfile

from src.catalog.coordinateextractor import CoordinateExtractor
from src.metaclasses import Singleton
from configparser import ConfigParser
from src.engine import RuleEngine
import configparser

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
        try:
            temp = reader['main']['outfolder']
            self.put('outfolder', temp)
            kb = reader['main']['datakb']
            dg = reader['main']['defaultdatafactory']
            engine = RuleEngine(kb,dg)
            self.put('dataRE', engine)
            kb = reader['main']['imagekb']
            dg = reader['main']['defaultimagefactory']
            engine = RuleEngine(kb,dg)
            self.put('imageRE', engine)
            temp = reader['main']['fromdate']
            self.put('fromdate', temp)
            temp = reader['main']['todate']
            self.put('todate', temp)
            # coordinates extraction
            temp_latitude = reader['image']['latitude']
            temp_longitude = reader['image']['longitude']
            temp_country = reader['image']['countryname']
            lat, lon = CoordinateExtractor.get_coordinates(temp_country, temp_latitude, temp_longitude)
            self.put('latitude', lat)
            self.put('latitude', lon)
            temp = reader['image']['area']
            self.put('area', float(temp))
            temp = reader['image']['imageresolution']
            self.put('imageresolution', int(temp))
            temp = reader['image']['format']
            self.put('format', temp)
            temp = reader['image']['imagetimeinterval']
            self.put('imagetimeinterval', float(temp))
            datalist = self.tolist(reader['data']['data'])
            self.put('data', datalist)
            temp = reader['data']['datatimeinterval']
            self.put('datatimeinterval', float(temp))
        except Exception as s:
            print(s)


def folderextraction(confcontent):
    tmp = tempfile.NamedTemporaryFile()
    handler = open(tmp.name, 'w')
    handler.write(confcontent)
    handler.flush()
    reader = configparser.ConfigParser()
    reader.read(tmp.name)
    try:
        temp = reader['main']['outfolder']
    except Exception as s:
        temp = None
    return temp

def mongoextraction(confcontent):
    tmp = tempfile.NamedTemporaryFile()
    handler = open(tmp.name, 'w')
    handler.write(confcontent)
    handler.flush()
    reader = configparser.ConfigParser()
    reader.read(tmp.name)
    try:
        temp = reader['main']['outfolder']
    except Exception as s:
        temp = None
    return temp
