package nuggetdb.db;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

public class Result {
	ArrayList<String> values = new ArrayList<String>();

	public Result(ResultSet rs) {
		try {
			int columns = rs.getMetaData().getColumnCount();
			for(int i = 0; i < columns; i++) {
				values.add(rs.getString(i+1));
			}
		} catch (SQLException e) {
			throw new RuntimeException(e);
		}
	}
	
	public int getInt(int index) {
		return Integer.valueOf(values.get(index));
	}

	public String getString(int index) {
		return values.get(index);
	}
	
	public String toString() {
		return values.toString();
	}

}
