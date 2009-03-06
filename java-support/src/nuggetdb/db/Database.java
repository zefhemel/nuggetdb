package nuggetdb.db;

import java.sql.DriverManager;
import java.sql.SQLException;

public class Database {
	static {
		try {
			Class.forName("com.mysql.jdbc.Driver").newInstance();
		} catch (InstantiationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private String hostname;
	private String username;
	private String password;
	private String database;

	public Database(String hostname, String username,
			String password, String database) {
		this.hostname = hostname;
		this.username = username;
		this.password = password;
		this.database = database;

	}
	java.sql.Connection conn = null;
	
	public Connection getConnection() {
		if(conn == null) {
			try {
				conn = DriverManager.getConnection("jdbc:mysql://" + hostname + "/" + database, username, password);
			} catch (SQLException e) {
				throw new RuntimeException(e);
			}
		}
		return new Connection(conn);
	}
}
