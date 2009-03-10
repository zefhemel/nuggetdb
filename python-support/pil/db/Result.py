
class Result(object):
    def __init__(self, rs):
        self.values = rs
	
    def getInt(self, index):
		return int(self.values[index])

    def getString(self, index):
		return str(values[index])
	}
	
    def getDateTime(self, index):
        return datetime.strptime('YYYY-MM-DD HH:MM:SS.mmmmm', str(values[index]))
	
    def __str__(self):
		return str(values)
