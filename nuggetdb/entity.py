import uuid
import nuggetdb.shard

class IllegalIdException(Exception):
    pass

class Entity(object):
    id = None
    updated = None
    ns = None
    _new = True

    def __init__(self, ns='', id=None, updated=None, new=True, **content):
        self.id = id
        for k, v in content.items():
            setattr(self, k, v)
        self.updated = updated
        self.ns = ns
        self._shard = None
        self._new = new

    def as_dict(self):
        d = {}
        for p in dir(self):
            if p in ['id', 'updated', 'ns']:
                continue
            if p.startswith('_'):
                continue
            if callable(getattr(self, p)):
                continue
            d[p] = getattr(self, p)
        return d

    def generate_id(self):
        return str(uuid.uuid4())

    def validate(self):
        # Check id characters
        if '/' in self.id:
            raise IllegalIdException("The following characters are not allowed in ids: /")

    def put(self, shard=None):
        if not self.id:
            self.id = self.generate_id()
        if shard:
            self.__shard = shard
        self.validate()
        self.__shard.put(self)

    @classmethod
    def all(cls):
        for s in nuggetdb.shard.shards.values():
            for e in s.all():
                yield e

    @classmethod
    def all_in_ns(cls, ns, order_by_date=None):
        for s in nuggetdb.shard.shards.values():
            for e in s.all_in_ns(ns, order_by_date):
                yield e
