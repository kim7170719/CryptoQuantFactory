import json
import os

class I18N:
    def __init__(self, lang='en', i18n_dir=None):
        self.lang = lang
        self.i18n_dir = i18n_dir or os.path.join(os.path.dirname(__file__))
        self.trans = self._load()
    def _load(self):
        path = os.path.join(self.i18n_dir, f'{self.lang}.json')
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    def t(self, key):
        return self.trans.get(key, key)
