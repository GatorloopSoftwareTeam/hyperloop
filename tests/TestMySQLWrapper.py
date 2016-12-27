import sys
sys.path.append('../')
import unittest
from MySQLWrapper import *
from mockito import *
import MySQLdb


class TestMySQLWrapper(unittest.TestCase):

    def setUp(self):
        self.mocked_conn = mock()
        self.mocked_cursor = mock()
        self.mocked_logging = mock()
        self.query = "test query"
        self.params = "test params"

        when(self.mocked_conn).commit().thenReturn(None)
        when(self.mocked_conn).cursor().thenReturn(self.mocked_cursor)
        when(MySQLdb).connect(host=any(str), user=any(str), passwd=any(str), db=any(str)).thenReturn(self.mocked_conn)

        self.wrapper = MySQLWrapper(self.mocked_logging)
        self.wrapper_spy = spy(self.wrapper)

    def tearDown(self):
        unstub()

    def test_instantiation(self):
        verify(MySQLdb, times=1).connect(
            host=Constants.MYSQL_HOST,
            user=Constants.MYSQL_USER,
            passwd=Constants.MYSQL_PASSWORD,
            db=Constants.MYSQL_DB)

        self.assertEqual(self.mocked_logging, self.wrapper.logging)

    def test_reset_connection(self):
        self.wrapper_spy.reset_connection()

        verify(MySQLdb, times=2).connect(
            host=Constants.MYSQL_HOST,
            user=Constants.MYSQL_USER,
            passwd=Constants.MYSQL_PASSWORD,
            db=Constants.MYSQL_DB)
        verify(self.wrapper_spy, times=1).reset_connection()

    def test_successful_execute(self):
        when(self.mocked_cursor).execute(self.query, self.params).thenReturn(None)

        self.wrapper.execute(self.query, self.params)

        verify(self.mocked_conn, times=1).cursor()
        verify(self.mocked_conn, times=1).commit()
        verify(self.mocked_cursor, times=1).execute(self.query, self.params)
        verify(self.mocked_cursor, times=1).close()

    def test_execute_exception(self):
        exception_msg = "Execution exception."
        when(self.mocked_cursor).execute(self.query, self.params).thenRaise(Exception(exception_msg))
        when(self.mocked_conn).rollback().thenReturn(None)

        self.wrapper.execute(self.query, self.params)

        verify(self.mocked_conn, times=1).cursor()
        verify(self.mocked_conn, times=0).commit()
        verify(self.mocked_cursor, times=1).execute(self.query, self.params)
        verify(self.mocked_cursor, times=1).close()
        verify(self.mocked_logging, times=1)\
            .debug("Encountered exception: " + exception_msg + ", when executing query: " + self.query)

    def test_rollback_exception(self):
        execution_exception_msg = "Execution exception."
        rollback_exception_msg = "Rollback exception"
        when(self.mocked_cursor).execute(self.query, self.params)\
            .thenRaise(Exception(execution_exception_msg))\
            .thenReturn(None)
        when(self.mocked_conn).rollback().thenRaise(Exception(rollback_exception_msg))
        when(self.wrapper_spy).reset_connection().thenReturn(None)

        self.wrapper_spy.execute(self.query, self.params)

        verify(self.mocked_conn, times=2).cursor()
        verify(self.mocked_conn, times=1).commit()
        verify(self.mocked_cursor, times=2).execute(self.query, self.params)
        verify(self.mocked_cursor, times=2).close()
        verify(self.wrapper_spy, times=1).reset_connection()
        verify(self.mocked_logging, times=1)\
            .debug("Encountered exception: " + execution_exception_msg + ", when executing query: " + self.query)
        verify(self.mocked_logging, times=1)\
            .debug("rollback failed with exception: " + rollback_exception_msg + " . Resetting and retrying query")
        verifyNoMoreInteractions(self.mocked_logging)

    def test_rollback_exception_retry(self):
        execution_exception_msg = "Execution exception."
        rollback_exception_msg = "Rollback exception"
        when(self.mocked_cursor).execute(self.query, self.params)\
            .thenRaise(Exception(execution_exception_msg))
        when(self.mocked_conn).rollback().thenRaise(Exception(rollback_exception_msg))
        when(self.wrapper_spy).reset_connection().thenReturn(None)

        self.wrapper_spy.execute(self.query, self.params)

        verify(self.mocked_conn, times=4).cursor()
        verify(self.mocked_conn, times=0).commit()
        verify(self.mocked_cursor, times=4).execute(self.query, self.params)
        verify(self.mocked_cursor, times=4).close()
        verify(self.wrapper_spy, times=3).reset_connection()
        verify(self.mocked_logging, times=4)\
            .debug("Encountered exception: " + execution_exception_msg + ", when executing query: " + self.query)
        verify(self.mocked_logging, times=4)\
            .debug("rollback failed with exception: " + rollback_exception_msg + " . Resetting and retrying query")
        verify(self.mocked_logging, times=1) \
            .error("Could not complete query: " + self.query + ". Aborting...")
        verifyNoMoreInteractions(self.mocked_logging)

if __name__ == '__main__':
    unittest.main()