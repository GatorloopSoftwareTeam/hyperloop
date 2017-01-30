import socket
import logging
import datetime
import constants
from drive_controller import DriveController


def start_listener(pod_data, sql_wrapper):
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('127.0.0.1', 6666))
    server_socket.listen(5)

    (client_socket, address) = server_socket.accept()

    while True:
        chunk = client_socket.recv(5)
        if chunk == "KILL\n":
            try:
                # stop the pod
                client_socket.send("KILLED\n")
                dc = DriveController()
                dc.send_kill_pod()
                logging.info("Pod kill power sent")
                break
            except socket.error, e:
                logging.debug("Socket error: " + str(e))
                client_socket.close()
                sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), "FAULT STATE"))
                pod_data.state = constants.STATE_FAULT

    client_socket.close()
    server_socket.close()
