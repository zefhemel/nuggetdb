package pil.json;

import java.util.Iterator;

import org.json.JSONException;
import org.json.JSONObject;

public class FromJsonString {
	public static JsonObject fromJsonString(String jsonString) {
		try {
			JSONObject json = new JSONObject(jsonString);
			JsonObject o = new JsonObject();
			for (Iterator<Object> iterator = json.keys(); iterator.hasNext();) {
				String key = (String) iterator.next();
				Object val = json.get(key);
				if(val instanceof String) {
					o.setString(key, (String) val);
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
