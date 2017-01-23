import socket
import logging
from drive_controller import DriveController


def start_listener():
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
                client_socket.close()

    server_socket.close()
