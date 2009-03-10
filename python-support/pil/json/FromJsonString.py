import simplejson
import pil.json.JsonObject

def fromJsonString(jsonString):
    try:
        json = simplejson.loads(jsonString)
        o = pil.json.JsonObject.JsonObject();
        for (Iterator<Object> iterator = json.keys(); iterator.hasNext();) {
            String key = (String) iterator.next();
            Object val = json.get(key);
            if(val instanceof String) {
                try {
                    Date d = JsonObject.dateFormat.parse((String) val);
                    o.setDateTime(key, d);
                } catch(Exception e) {
                    o.setString(key, (String) val);						
                }
            } else if(val instanceof Integer) {
                o.setInt(key, (Integer)val);
            } else {
                throw new RuntimeException("Unkown value type: " + val.getClass());
            }
        }
        return o;
		} catch (JSONException e) {
			return null;
		}
	}
}
