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

    def _db_id(self, entity):
        if entity.ns:
            return entity.ns + '/' + entity.id
        else:
            return entity.id

    def _extract_ns_id(self, db_id):
        parts = db_id.split('/')
        if len(parts) == 1: # No namepsace
            return (None, db_id)
        else:
            return ('/'.join(parts[0:-1]), parts[-1])

    def put(self, entity):
        conn = self.get_connection()
        c = conn.cursor()
        if entity._new:
            c.execute('INSERT INTO ' + self.table_prefix + 'entity VALUES (%s, NOW(), %s)', (self._db_id(entity), pickle.dumps(entity.as_dict())))
            entity._new = False
        else:
            c.execute('UPDATE ' + self.table_prefix + 'entity SET updated = NOW(), content = %s WHERE id = %s;', (pickle.dumps(entity.as_dict()), self._db_id(entity)))
        conn.commit()

    def _entity_from_db_row(self, row):
        (ns, id) = self._extract_ns_id(row[0])
        return Entity(ns=ns, id=id, updated=row[1], new=False, **pickle.loads(row[2]))

    def all(self):
        c = self.get_connection().cursor()
        c.execute('SELECT * FROM ' + self.table_prefix + 'entity')
        for row in c:
            yield self._entity_from_db_row(row)

    def all_in_ns(self, ns, order_by_date=None):
        c = self.get_connection().cursor()
        if order_by_date:
            order_by = 'ORDER BY updated %s' % order_by_date
        else:
            order_by = ''
        if ns:
            c.execute('SELECT * FROM ' + self.table_prefix + 'entity WHERE id LIKE %s ' + order_by, ns + '/%')
        else:
            c.execute('SELECT * FROM ' + self.table_prefix + 'entity' + order_by)
        for row in c:
            yield self._entity_from_db_row(row)

    def create(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SHOW TABLES;')
        if not self.table_prefix+'entity' in [r[0] for r in c.fetchall()]:
            c = conn.cursor()
            c.execute('''CREATE TABLE ''' + self.table_prefix + '''entity (
                          `id` varchar(200) NOT NULL,
                          `updated` timestamp default NOW(),
                          `content` mediumblob,
                          PRIMARY KEY  (`id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=latin1''')
            conn.commit()

    def __repr__(self):
        return '(Shard: ' + self.name + ')'

