
class Connection(object):
    import pil.db.Result

    def __init__(self, conn):
        self.conn = conn

    def query(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        results = []
        for row in c:
            results.append(pil.db.Result.Result(row))
        return results

    def updateQuery(sql):
        c = self.conn.cursor()
        c.execute(sql)
