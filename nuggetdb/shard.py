import cPickle as pickle
import uuid

shards = {}

def register(shard):
    shards[shard.name] = shard

class Shard(object):
    name = None
    connection = None

    def __init__(self, name, driver, user, passwd, db):
        self.name = str(name)
        self.driver = driver
        self.user = user
        self.passwd = passwd
        self.db = db

    def get_connection(self):
        if not self.connection:
            self.connection = self.driver.connect(user=self.user, passwd=self.passwd, db=self.db)
        return self.connection

    def put(self, entity):
        conn = self.get_connection()
        c = conn.cursor()
        if entity._new:
            c.execute('''INSERT INTO Entity VALUES (%s, NOW(), %s)''', (entity.id, pickle.dumps(entity.as_dict())))
            entity._new = False
        else:
            c.execute('''UPDATE Entity SET updated = NOW, content = %s WHERE id = %s;''',  (pickle.dumps(entity.as_dict()), entity.id))
        conn.commit()

    def all(self):
        c = self.get_connection().cursor()
        c.execute('SELECT * FROM Entity')
        for (id, updated, content) in c:
            yield Entity(id, pickle.loads(content), updated, new=False)

    def __repr__(self):
        return '(Shard: ' + self.name + ')'

