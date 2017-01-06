import Queue
import thread


class DBQueue:
    def __init__(self, sql_wrapper):
        self.queue = Queue.Queue()
        self.sql_wrapper = sql_wrapper
        thread.start_new_thread(self.process_queue, ())

    def process_queue(self):
        while True:
            if not self.queue.empty():
                query_struct = self.queue.get(False)
                self.sql_wrapper.execute_from_queue(query_struct.query, query_struct.params)

    def push(self, query_struct):
        self.queue.put(query_struct)
