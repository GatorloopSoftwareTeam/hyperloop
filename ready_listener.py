import socket
import constants
import datetime


def start_listener(logging, pod_data, sql_wrapper):
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
                client_socket.send("READY\n")
                logging.info("Move to ready signal received")
                break
            except socket.error, e:
                logging.debug("Socket error: " + str(e))
                client_socket.close()
                sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), "FAULT STATE"))
                pod_data.state = constants.STATE_FAULT

    server_socket.close()
