import yaml
import io
from random import sample
from py_rules.engine import RuleEngine
from py_rules.storages import RuleStorage
import ast


class EngineSelector:
    def __init__(self, knowledgebase, ddefaultgrabber):
        self.defaultgrabber = ddefaultgrabber
        self.kbase = self.load_knowledgebase(knowledgebase)

    def load(self, rule_content):
        parser = RuleParser(rule_content)
        return parser.load()

    def load_knowledgebase(self, knowledgebase):
        with open(knowledgebase, 'r', encoding='utf-8') as file:
            content = file.read()
            structure = ast.literal_eval(content)
            structure = list(filter(lambda x: x[1], structure))
            structure = list(map(lambda x: x[0], structure))
            structure = list(map(self.load, structure))
        return structure

    def match(self, features):
        engine = RuleEngine(features)
        results = list(map(engine.evaluate, self.kbase))
        results = list(map(lambda x: x['enginefactory'], results))
        results = set(results)
        if 'None' in results:
            results.remove('None')
        match = self.defaultgrabber if len(results) == 0 else sample(results, 1)[0]
        return match




yaml.Dumper.ignore_aliases = lambda *args: True

class RuleParser(RuleStorage):

    def __init__(self, content):
        super().__init__()
        self.content = content

    def load(self):
        f = io.StringIO(self.content)
        data = yaml.load(f, Loader=yaml.FullLoader)
        return self.parser.parse(data)

    def store(self, rule):
        pass

