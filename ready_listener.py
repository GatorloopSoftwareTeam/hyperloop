import socket
import logging
from states import ready_state
from drive_controller import DriveController


def start_listener(pod_data, sql_wrapper):
    logging.debug("LISTENING FOR READY")
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('127.0.0.1', 6668))
    server_socket.listen(5)

    (client_socket, address) = server_socket.accept()

    while True:
        chunk = client_socket.recv(7)
        if chunk == "READY\n":
            try:
                # stop the pod
                client_socket.send("READY\n")
                logging.info("Move to ready signal received")
                break
            except socket.error, e:
                client_socket.close()

    client_socket.close()
    server_socket.close()
    ready_state.start(pod_data, sql_wrapper)
