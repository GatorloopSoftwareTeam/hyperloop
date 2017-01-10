import socket

TCP_IP = '192.168.0.10'
TCP_PORT = 3000
BUFFER_SIZE = 1024

PING_DATA_ID = "0x10"
PING_PAYLOAD_LENGTH = "0x00"
ping_request = PING_DATA_ID + PING_PAYLOAD_LENGTH

PING_REPLY_ID = "0x50"
PING_REPLY_PAYLOAD_LENGTH = "0x02"

START_SCU_DATA_ID = "0x11"
START_SCU_PAYLOAD_LENGTH = "0x00"
start_scu_request = START_SCU_DATA_ID + START_SCU_PAYLOAD_LENGTH

START_SCU_REPLY_ID = "0x51"
START_SCU_REPLY_PAYLOAD_LENGTH = "0x02"

START_LOGGING_DATA_ID = "0x12"
START_LOGGING_PAYLOAD_LENGTH = "0x00"
start_logging_request = START_LOGGING_DATA_ID + START_LOGGING_PAYLOAD_LENGTH

START_LOGGING_REPLY_ID = "0x52"
START_LOGGING_REPLY_PAYLOAD_LENGTH = "0x08"

STOP_LOGGING_DATA_ID = "0x13"
STOP_LOGGING_PAYLOAD_LENGTH = "0x00"
stop_logging_request = STOP_LOGGING_DATA_ID + STOP_LOGGING_PAYLOAD_LENGTH

STOP_LOGGING_REPLY_ID = "0x53"
STOP_LOGGING_REPLY_PAYLOAD_LENGTH = "0x08"

STOP_SCU_DATA_ID = "0x14"
STOP_SCU_PAYLOAD_LENGTH = "0x00"
stop_scu_request = STOP_SCU_DATA_ID + STOP_SCU_PAYLOAD_LENGTH

STOP_SCU_REPLY_ID = "0x54"
STOP_SCU_REPLY_PAYLOAD_LENGTH = "0x02"

AVAILABLE_SD_DATA_ID = "0x15"
AVAILABLE_SD_PAYLOAD_LENGTH = "0x00"
available_sd_request = AVAILABLE_SD_DATA_ID + AVAILABLE_SD_PAYLOAD_LENGTH

AVAILABLE_SD_REPLY_ID = "0x55"
AVAILABLE_SD_REPLY_PAYLOAD_LENGTH = "0x05"

CLEAR_LOGS_DATA_ID = "0x16"
CLEAR_LOGS_PAYLOAD_LENGTH = "0x00"
clear_logs_request = CLEAR_LOGS_DATA_ID + CLEAR_LOGS_PAYLOAD_LENGTH

CLEAR_LOGS_REPLY_ID = "0x56"
CLEAR_LOGS_REPLY_PAYLOAD_LENGTH = "0x07"

HEARTBEAT_DATA_ID = "0x17"
HEARTBEAT_PAYLOAD_LENGTH = "0x00"
heartbeat_request = HEARTBEAT_DATA_ID + HEARTBEAT_PAYLOAD_LENGTH

HEARTBEAT_REPLY_ID = "0x57"
HEARTBEAT_REPLY_PAYLOAD_LENGTH = "0x02"


def get_request(index):
    global ping_request,\
        start_scu_request,\
        start_logging_request,\
        stop_logging_request,\
        stop_scu_request,\
        available_sd_request,\
        clear_logs_request,\
        heartbeat_request

    return {
        1: ping_request,
        2: start_scu_request,
        3: start_logging_request,
        4: stop_logging_request,
        5: stop_scu_request,
        6: available_sd_request,
        7: clear_logs_request,
        8: heartbeat_request
    }.get(index, None)


def get_response_size_in_bytes(index):
    global PING_REPLY_PAYLOAD_LENGTH,\
        START_SCU_REPLY_PAYLOAD_LENGTH,\
        START_LOGGING_REPLY_PAYLOAD_LENGTH,\
        STOP_LOGGING_PAYLOAD_LENGTH,\
        STOP_SCU_REPLY_PAYLOAD_LENGTH,\
        AVAILABLE_SD_REPLY_PAYLOAD_LENGTH,\
        CLEAR_LOGS_REPLY_PAYLOAD_LENGTH,\
        HEARTBEAT_REPLY_PAYLOAD_LENGTH

    return {
        1: PING_REPLY_PAYLOAD_LENGTH,
        2: START_SCU_REPLY_PAYLOAD_LENGTH,
        3: START_LOGGING_REPLY_PAYLOAD_LENGTH,
        4: STOP_LOGGING_REPLY_PAYLOAD_LENGTH,
        5: STOP_SCU_REPLY_PAYLOAD_LENGTH,
        6: AVAILABLE_SD_REPLY_PAYLOAD_LENGTH,
        7: CLEAR_LOGS_REPLY_PAYLOAD_LENGTH,
        8: HEARTBEAT_REPLY_PAYLOAD_LENGTH
    }.get(index, None)


def get_expected_response_id(index):
    global PING_REPLY_ID,\
        START_SCU_REPLY_ID,\
        START_LOGGING_REPLY_ID,\
        STOP_LOGGING_REPLY_ID,\
        STOP_SCU_REPLY_ID,\
        AVAILABLE_SD_REPLY_ID,\
        CLEAR_LOGS_REPLY_ID,\
        HEARTBEAT_REPLY_ID

    return {
        1: PING_REPLY_ID,
        2: START_SCU_REPLY_ID,
        3: START_LOGGING_REPLY_ID,
        4: STOP_LOGGING_REPLY_ID,
        5: STOP_SCU_REPLY_ID,
        6: AVAILABLE_SD_REPLY_ID,
        7: CLEAR_LOGS_REPLY_ID,
        8: HEARTBEAT_REPLY_ID
    }.get(index, None)


while True:
    selection = raw_input("Which command would you like to send?\n"
                          "1. Ping\n"
                          "2. Start SCU\n"
                          "3. Start Logging\n"
                          "4. Stop Logging\n"
                          "5. Stop SCU\n"
                          "6. Available SD\n"
                          "7. Clear Logs\n"
                          "8. Heartbeat\n")

    int_selection = 1
    try:
        global int_selection
        int_selection = int(selection)
        if int_selection < 1 or int_selection > 8:
            raise ValueError
    except ValueError:
        print "Please enter a selection 1-8"
        continue
    
    request = str(get_request(int_selection))
    request = 0x10
    print "Request: " + str(request)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send("10")
    # 2 bytes for request id and payload length
    #data = s.recv(2 + int(get_response_size_in_bytes(int_selection)))
    data = s.recv(1024)
    s.close()

    print "received data:", data
