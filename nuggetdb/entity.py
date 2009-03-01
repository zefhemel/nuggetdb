
class Entity(object):
    def __init__(self, id=None, content={}, updated=None, new=True):
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

    def put(self, shard=None):
        if shard:
            self.__shard = shard
        if not self.id:
            self.id = str(uuid.uuid4())
        self.__shard.put(self)

    @classmethod
    def all(cls):
        for s in shards.values():
            for e in s.all():
                yield e
