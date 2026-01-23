from rule import Rule

class RuleEngine:
    def __init__(self, knowledgebase, ddefaultgrabber):
        self.kbase = dict()
        self.defaultgrabber = ddefaultgrabber
        filehandler = open(knowledgebase)
        for line in filehandler:
            line = line.removesuffix('\n')
            rule, function = line.split('---')
            self.kbase[rule] = function

    def match(self, features):
        match = self.defaultgrabber
        keys = list(self.kbase.keys())
        found = False
        i = 0
        while found is False and i < len(keys):
            key = keys[i]
            rule = Rule(key)
            found = rule.match(features)
            if found:
                match = self.kbase[key]
            i += 1
        return match
