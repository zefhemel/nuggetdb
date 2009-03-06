package pil.json;

import java.util.HashMap;

import org.json.JSONException;
import org.json.JSONObject;

public class JsonObject {
	HashMap<String, Integer> ints = new HashMap<String, Integer>();
	HashMap<String, String> strings = new HashMap<String, String>();
	
	public String getString(String key) {
		return strings.get(key);
	}
	
	public void setString(String key, String value) {
		strings.put(key, value);
	}
	
	public int getInt(String key) {
		return ints.get(key);
	}
	
	public void setInt(String key, int value) {
		ints.put(key, value);
	}
	
	public String toJson() {
		try {
			JSONObject json = new JSONObject();
			for(String key : ints.keySet()) {
					json.put(key, ints.get(key));
			}
			for(String key : strings.keySet()) {
				json.put(key, strings.get(key));
			}
			return json.toString();
		} catch (JSONException e) {
			throw new RuntimeException(e);
		}
	}
}
