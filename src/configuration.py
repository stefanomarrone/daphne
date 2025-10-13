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
        reader.read(f'run/{inifile}')
        #MAIN
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
        #IMAGE
        temp = reader['image']['longitude']
        if temp != '':
            self.put('longitude', float(temp))
        else:
            self.put('longitude', '')
        temp = reader['image']['latitude']
        if temp != '':
            self.put('latitude', float(temp))
        else:
            self.put('latitude', '')
        #temp = reader['image']['area']
        #self.put('area', float(temp))
        temp = reader['image']['countryname']
        self.put('countryname', temp)
        temp = reader['image']['imageresolution']
        self.put('imageresolution', int(temp))
        temp = reader['image']['format']
        self.put('format', temp)
        #temp = reader['image']['imagetimeinterval']
        #self.put('imagetimeinterval', float(temp))
        temp = reader['image'].get('resolutions', [])
        temp = self.tolist(temp)
        self.put('resolutions', temp)
        temp = reader['image'].get('productTypes', [])
        temp = self.tolist(temp)
        self.put('productTypes', temp)
        temp = reader['image'].get('providers', [])
        temp = self.tolist(temp)
        self.put('providers', temp)
        temp = reader['image'].get('openData', True)
        self.put('openData', bool(temp))
        temp = reader['image'].get('maxCloudCoveragePercent', 100)
        self.put('maxCloudCoveragePercent', int(temp))


        #DATA
        datalist = self.tolist(reader['data']['data'])
        self.put('data', datalist)
        temp = reader['data']['datatimeinterval']
        self.put('datatimeinterval', float(temp))

