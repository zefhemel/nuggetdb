import uuid
import nuggetdb.shard

class Entity(object):
    id = None
    updated = None

    def __init__(self, id=None, updated=None, new=True, **content):
        self.id = id
        for k, v in content.items():
            setattr(self, k, v)
        self.updated = updated
        self._shard = None
        self._new = new

    def as_dict(self):
        d = {}
        for p in dir(self):
            if p in ['id', 'updated']:
                continue
            if p.startswith('_'):
                continue
            if callable(getattr(self, p)):
                continue
            d[p] = getattr(self, p)
        return d

    def generate_id(self):
        return str(uuid.uuid4())

    def put(self, shard=None):
        if shard:
            self.__shard = shard
        if not self.id:
            self.id = self.generate_id()
        self.__shard.put(self)

    @classmethod
    def all(cls):
        for s in nuggetdb.shard.shards.values():
            for e in s.all():
                yield e

class Model(Entity):

    def prefix(self):
        return self.__class__.__name__ + '/'

    def generate_id(self):
        return self.prefix() + Entity.generate_id(self)
    
    def put(self, shard=None):
        if self.id and not self.id.startswith(self.prefix()):
            self.id = self.prefix() + self.id
        Entity.put(self, shard)

    @classmethod
    def all(cls):
        for s in nuggetdb.shard.shards.values():
            for e in s.all_with_id(cls.__name__ + '/%'):
                yield e
