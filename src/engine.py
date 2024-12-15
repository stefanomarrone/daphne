import yaml
import io
from random import sample
from py_rules.engine import RuleEngine
from py_rules.storages import RuleStorage
import ast

from src.utils import get_content

yaml.Dumper.ignore_aliases = lambda *args: True

class EngineSelector:
    def __init__(self, knowledge_base_filename, ddefaultgrabber, kb_folder):
        self.defaultgrabber = ddefaultgrabber
        self.kbase = self.load_knowledgebase(kb_folder, knowledge_base_filename)

    def load(self, rule_content):
        parser = RuleParser(rule_content)
        retval = parser.load()
        return retval

    def load_knowledgebase(self, kb_folder, knowledge_base_filename):
        with open(kb_folder + knowledge_base_filename, 'r', encoding='utf-8') as file:
            content = file.read()
            structure = ast.literal_eval(content)
            structure = list(filter(lambda x: x[1], structure))
            structure = list(map(lambda x: kb_folder + x[0], structure))
            structure = list(map(get_content, structure))
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

