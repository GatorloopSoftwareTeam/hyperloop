import MySQLdb
import constants
import datetime


class MySQLWrapper:
    def __init__(self, logging):
        self._conn = MySQLdb.connect(host=constants.MYSQL_HOST,
                                     user=constants.MYSQL_USER,
                                     passwd=constants.MYSQL_PASSWORD,
                                     db=constants.MYSQL_DB)
        self.logging = logging

    def execute(self, query, params, retry_count=0):
        cursor = self._conn.cursor()
        try:
            cursor.execute(query, params)
            self._conn.commit()
            cursor.close()
        except MySQLdb.OperationalError, e:
            # The db has gone down
            cursor.close()
            if retry_count > 20:
                # this is going to fail out of initialization or initiate emergency braking
                raise MySQLdb.OperationalError(e)

            self.execute(query, params, retry_count + 1)

        except Exception, e:
            cursor.close()
            self.logging.debug("Encountered exception: " + str(e) + ", when executing query: " + query)
            try:
                self._conn.rollback()

            except Exception, e:
                self.logging.debug("rollback failed with exception: " + str(e) + " . Resetting and retrying query")
                if retry_count > 2:
                    self.logging.error("Could not complete query: " + str(query) + ". Aborting...")
                    return

                self.reset_connection()
                self.execute(query, params, retry_count + 1)

    def reset_connection(self):
        self._conn = MySQLdb.connect(host=constants.MYSQL_HOST,
                                     user=constants.MYSQL_USER,
                                     passwd=constants.MYSQL_PASSWORD,
                                     db=constants.MYSQL_DB)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()
