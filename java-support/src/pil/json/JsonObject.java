package pil.json;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;

import org.json.JSONException;
import org.json.JSONObject;

public class JsonObject {
	HashMap<String, Object> data = new HashMap<String, Object>();

	static public SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.S");
	
	public String getString(String key) {
		return data.get(key).toString();
	}
	
	public void setString(String key, String value) {
		data.put(key, value);
	}
	
	public int getInt(String key) {
		return (Integer) data.get(key);
	}
	
	public void setInt(String key, int value) {
		data.put(key, value);
	}
	
	public void setDateTime(String key, Date value) {
		data.put(key, value);
	}
	
	public Date getDateTime(String key) {
		return (Date) data.get(key);
	}
	
	public void set(String key, Object value) {
		data.put(key, value);
	}
	
	public Object get(String key) {
		return data.get(key);
	}
	
	public String toJson() {
		try {
			// "yyyy.MM.dd G 'at' HH:mm:ss z"
			JSONObject json = new JSONObject();
			for(String key : data.keySet()) {
				Object value = data.get(key);
				if(value instanceof Date) {
					json.put(key, dateFormat.format((Date)value));
				} else {
					json.put(key, data.get(key));
				}
			}
			return json.toString();
		} catch (JSONException e) {
			throw new RuntimeException(e);
		}
	}
}
