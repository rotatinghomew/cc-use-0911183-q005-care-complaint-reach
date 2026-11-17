from pathlib import Path
import json

from .channels import *
from .coverage import *
from .followthrough import *


class Application:
    def __init__(self, store):
        self.store = store

    def seed(self):
        directory = Path(__file__).resolve().parent.parent / 'fixtures'
        for path in sorted(directory.glob('*.json')):
            if not self.store.all(path.stem):
                self.store.put_many(path.stem, json.loads(path.read_text(encoding='utf-8')))

    def demo(self):
        return {'coverage': observed_coverage(self.store), 'groups': explicit_groups(self.store), 'followups': open_followups(self.store)}

    def check(self):
        value = self.demo()
        return {'status': 'ok', 'summary': value}

    def call(self, method, route, payload):
        if method == 'GET' and route == 'summary':
            return self.demo()
        if method == 'POST' and route == 'report':
            return {'revision': save_report(self.store, payload)}
        if method == 'POST' and route == 'close':
            return close_report(self.store, payload['id'])
        if method == 'POST' and route == 'reply':
            return {'revision': record_reply(self.store, payload)}
        raise KeyError('接口不存在')
