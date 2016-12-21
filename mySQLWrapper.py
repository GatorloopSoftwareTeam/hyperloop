import MySQLdb
import Constants
import datetime


class MySQLWrapper:

    def __init__(self, logging):
        self._conn = MySQLdb.connect(host=Constants.MYSQL_HOST,
                               user=Constants.MYSQL_USER,
                               passwd=Constants.MYSQL_PASSWORD,
                               db=Constants.MYSQL_DB)
        self.logging = logging

    def execute(self, query, params):
        cursor = self._conn.cursor()
        try:
            cursor.execute(query, params)
            self._conn.commit()
            self.logging.debug("Committed to db")
        except Exception, e:
            cursor.close()
            self.logging.debug("Encountered exception: " + str(e) + " when executing query: " + query)
            try:
                self._conn.rollback()
            except Exception, e:
                self.logging.debug("rollback failed with exception: " + str(e) + " retrying query")
                self.logging.debug("connection is probably stale. Resetting and retrying query")
                self.reset_connection()
                self.execute(query, params)

    def reset_connection(self):
        self._conn = MySQLdb.connect(host=Constants.MYSQL_HOST,
                                     user=Constants.MYSQL_USER,
                                     passwd=Constants.MYSQL_PASSWORD,
                                     db=Constants.MYSQL_DB)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

