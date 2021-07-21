import sqlite3

class Database:
	def __init__(self,db):
		self.conn = sqlite3.connect(db)
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS SAMPLE_METADATA_TABLE (FILE_ID INTEGER, ROW_ID INTEGER, ATTR_ID TEXT, ATTR_VAL INTEGER)")
		self.cur.execute("CREATE TABLE IF NOT EXISTS ANALYZED_DATA_TABLE (FILE_ID INTEGER, ROW_ID INTEGER, ATTR_ID TEXT, ATTR_VAL INTEGER)")

		self.conn.commit()

	def fetch(self, ATTR_VAL=''):
		self.cur.execute("SELECT * from SAMPLE_METADATA_TABLE where ATTR_VAL LIKE ?", ('%'+ATTR_VAL+'%',))
		rows=self.cur.fetchall()
		return rows

	def fetch2(self,query):
		self.cur.execute(query)
		rows=self.cur.fetchall()
		return rows

	def insert(self, ROW_ID, ATTR_ID, ATTR_VAL):
		self.cur.execute("INSERT INTO SAMPLE_METADATA_TABLE values (null, ?,?,?,?)", (ROW_ID, ATTR_ID, ATTR_VAL))
		self.conn.commit()

	def remove(self, FILE_ID):
		self.cur.execute("DELETE FROM SAMPLE_METADATA_TABLE WHERE FILE_ID=?",(FILE_ID,))
		self.conn.commit()

	def update(self, FILE_ID, ROW_ID, ATTR_ID, ATTR_VAL):
		self.cur.execute("UPDATE SAMPLE_METADATA_TABLE SET ATTR_VAL = ?, ROW_ID = ?, ATTR_ID = ? WHERE FILE_ID = ?",
			(ATTR_VAL, ROW_ID, ATTR_ID, FILE_ID))
		self.conn.commit()

	def __del__(self):
		self.conn.close()

