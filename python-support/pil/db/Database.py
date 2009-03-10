import MySQLdb

class Database(object):
    import pil.db.Connection

    def __init__(self, hostname, username, password, database):
		self.hostname = hostname
		self.username = username
		self.password = password
		self.database = database
        self.conn = None

    def getConnection(self):
        if not self.conn:
            self.conn = MySQLdb.connect(host=self.hostname, user=self.username, passwd=self.password, db=self.database)
		return pil.db.Connection.Connection(self.conn)
