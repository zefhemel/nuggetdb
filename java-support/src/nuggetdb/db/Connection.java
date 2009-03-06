package nuggetdb.db;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.LinkedHashSet;

public class Connection {
	private java.sql.Connection conn;
	public Connection(java.sql.Connection conn) {
		this.conn = conn;
	}
	public ArrayList<Result> query(String sql) {
		try {
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery(sql);
			ArrayList<Result> results = new ArrayList<Result>();
			while(rs.next()) {
				results.add(new Result(rs));
			}
			return results;
		} catch (SQLException e) {
			throw new RuntimeException(e);
		}
	}
}
