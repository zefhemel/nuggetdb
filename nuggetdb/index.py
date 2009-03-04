from nuggetdb.entity import Entity
from nuggetdb.shard import shards
import re

py_type_to_sql_type = {
        int: 'INT',
        str: 'VARCHAR(255)',
        unicode: 'VARCHAR(255)'
}

class Index(object):
    shard = None # Shard to store the index in
    columns = []
    column_types = [] # Python types of columns listed above
    ns = None

    def __init__(self, ns=None, columns=[], column_types=[], shard=None):
        self.ns = ns
        self.columns = columns
        self.column_types = column_types
        self.shard = shard

    def _tablify_name(self, name):
        return re.sub('[^a-zA-Z0-9]', '_', name)

    def _table_name(self):
        if self.ns:
            return self._tablify_name('index_' + self.ns + '_' + '_'.join(self.columns))
        else:
            return self._tablify_name('index_' + '_'.join(self.columns))

    def create(self):
        """Creates index table if not present"""
        conn = self.shard.get_connection()
        c = conn.cursor()
        c.execute('SHOW TABLES;')
        if not self._table_name() in [r[0] for r in c.fetchall()]:
            column_defs = []
            i = 0
            for i in range(len(self.columns)):
                column_defs.append(self.columns[i] + ' ' + py_type_to_sql_type[self.column_types[i]] + ' NOT NULL')
            sql = '''CREATE TABLE %s (
                        entity_id VARCHAR(200) NOT NULL UNIQUE,
                        %s,
                        updated TIMESTAMP NOT NULL DEFAULT NOW(),
                        shard VARCHAR(20) NOT NULL,
                        PRIMARY KEY (%s, entity_id)
                     ) ENGINE=InnoDB;''' % (self._table_name(), ','.join(column_defs), ', '.join(self.columns))
            c = conn.cursor()
            c.execute(sql)

    def add_entry(self, entity):
        conn = self.shard.get_connection()
        c = conn.cursor()
        vals = []
        for col in self.columns:
            vals.append('\'' + conn.escape_string(str(getattr(entity, col))) + '\'')
        c.execute('INSERT INTO %s (entity_id, shard, %s) VALUES (\'%s\', \'%s\', %s);' % 
                (self._table_name(), ', '.join(self.columns), conn.escape_string(entity._shard._db_id(entity)),  entity._shard.name, ', '.join(vals)))
        conn.commit()

    def has_entry(self, entity):
        conn = self.shard.get_connection()
        c = conn.cursor()
        c.execute('SELECT entity_id FROM ' + self._table_name() + ' WHERE entity_id = %s LIMIT 1', entity._shard._db_id(entity))
        return len(list(c)) == 1

    def lookup(self, **values):
        conn = self.shard.get_connection()
        wheres = []
        for (c, v) in values.items():
            if not c in self.columns:
                raise Exception("This index is not capable of looking up column %s" % c)
            wheres.append('%s = \'%s\'' % (c, conn.escape_string(str(v))))
        c = conn.cursor()
        c.execute('SELECT entity_id, shard FROM %s WHERE %s;' % (self._table_name(), ' AND '.join(wheres)))
        for (id, shard_id) in c:
            yield Entity.get(id, shards[shard_id])

    def update(self):
        for e in Entity.all_in_ns(self.ns, order_by_date='desc'):
            print e.id, e.updated
            if self.has_entry(e):
                print 'Quittin'
                break
            self.add_entry(e)

