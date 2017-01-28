import socket
import logging
import constants
import datetime
import states.brake_state


def start_listener(pod_data, sql_wrapper, drive_controller):
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
                time_since_push = (datetime.datetime.now() - pod_data.push_start_time)
                while time_since_push.total_seconds() < constants.TOTAL_PUSH_TIME:
                    logging.debug("Brake requested. Cannot brake for " + str(
                        (constants.TOTAL_PUSH_TIME - time_since_push).total_seconds()) + "seconds")

                # initiate emergency brake state
                states.brake_state.start(pod_data, sql_wrapper, drive_controller)
                client_socket.send("EBRAKED\n")
                logging.info("Pod emergency brake sent")
                break
            except socket.error, e:
                logging.debug("Socket error: " + str(e))
                client_socket.close()
                sql_wrapper.execute("""INSERT INTO states VALUES (NULL,%s,%s)""",
                                    (datetime.datetime.now().strftime(constants.TIME_FORMAT), "FAULT STATE"))
                pod_data.state = constants.STATE_FAULT

    server_socket.close()
