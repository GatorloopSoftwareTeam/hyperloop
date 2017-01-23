import socket
import logging
import constants
import datetime
import states.emergency_brake_state


def start_listener(pod_data):
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('127.0.0.1', 6667))
    server_socket.listen(5)

    (client_socket, address) = server_socket.accept()

    while True:
        chunk = client_socket.recv(7)
        if chunk == "EBRAKE\n":
            try:
                # do not initiate brake until pusher timeout is reached
                while (datetime.datetime.now() - pod_data.push_start_time).total_seconds() > constants.TOTAL_PUSH_TIME:
                    continue
                # initiate emergency brake state
                states.emergency_brake_state.start()
                client_socket.send("EBRAKED\n")
                logging.info("Pod emergency brake sent")
                break
            except socket.error, e:
                client_socket.close()

    client_socket.close()
    server_socket.close()
