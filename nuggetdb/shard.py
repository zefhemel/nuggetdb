import cPickle as pickle
from nuggetdb.entity import Entity

shards = {}

def register(shard):
    global shards
    shards[shard.name] = shard

def random_pick():
    """Picks a shard at random."""
    import random
    options = list(shards.values())
    rnd = random.randint(0, len(options) - 1)
    return options[rnd]

class Shard(object):
    name = None
    connection = None

    def __init__(self, name, driver, user, passwd, db, table_prefix = ''):
        self.name = str(name)
        self.driver = driver
        self.user = user
        self.passwd = passwd
        self.db = db
        self.table_prefix = table_prefix

    def get_connection(self):
        if not self.connection:
            self.connection = self.driver.connect(user=self.user, passwd=self.passwd, db=self.db)
        return self.connection

    def put(self, entity):
        conn = self.get_connection()
        c = conn.cursor()
        if entity._new:
            c.execute('INSERT INTO ' + self.table_prefix + 'entity VALUES (%s, NOW(), %s)', (entity.id, pickle.dumps(entity.as_dict())))
            entity._new = False
        else:
            c.execute('UPDATE ' + self.table_prefix + 'entity SET updated = NOW(), content = %s WHERE id = %s;', (pickle.dumps(entity.as_dict()), entity.id))
        conn.commit()

    def all(self):
        c = self.get_connection().cursor()
        c.execute('SELECT * FROM ' + self.table_prefix + 'entity')
        for (id, updated, content) in c:
            yield Entity(id, pickle.loads(content), updated, new=False)

    def create(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SHOW TABLES;')
        if not self.table_prefix+'entity' in [r[0] for r in c.fetchall()]:
            c = conn.cursor()
            c.execute('''CREATE TABLE ''' + self.table_prefix + '''entity (
                          `id` varchar(200) NOT NULL,
                          `updated` datetime default NULL,
                          `content` mediumblob,
                          PRIMARY KEY  (`id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=latin1''')
            conn.commit()

    def __repr__(self):
        return '(Shard: ' + self.name + ')'

