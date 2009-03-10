date_format = '%Y-%m-%d %H:%M:%S'

class JsonObject(object):
	
    def __init__(self):
        self.data = {}

    def getString(self, key):
        return str(self.data[key])
	
    def setString(self, key, value):
		self.data[key] = value
	
    def getInt(self, key):
		return int(self.data[key])
	
    def setInt(self, key, value):
		self.data[key] = value
	
	def setDateTime(self, key, value) {
		self.data[key] = value
	
	def getDateTime(self, key) {
		return self.date[key]
	
	def set(self, key, value) {
		self.data[key] = value
	}
	
	public Object get(String key) {
		return data.get(key)
	
	def toJson() {
        return simplejson.dumps(self.data)
	}
}
