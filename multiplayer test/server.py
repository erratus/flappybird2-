import socket

host = "127.0.0.1"  # Use localhost for testing
port = 12345

cli_datas = []
cli_datas.append(0)  # Initial ID
cli_data_next_count = 1


def re_id(spl, cli_data_next_count):
    spl[-1] = str(cli_data_next_count)
    ret_str = ":".join(spl)  # Efficient string joining using join()
    return ret_str


def re_message(cli_datas):
    mesaj = ";".join([str(i) for i in cli_datas])
    return mesaj


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")

    s.bind((host, port))
    print("Socket binding to address {} and port {}".format(host, port))

    s.listen(5)  # Listen for up to 5 incoming connections
    print("Socket listening")

except socket.error as msg:
    print("Error:", msg)
    exit()  # Exit the program on error

while True:
    try:
        c, addr = s.accept()  # Accept connections using try-except for error handling
        print("Connection from:", addr)

        userdata = c.recv(1024).decode("utf-8")

        spl = userdata.split(":")
        # print("User data = ",spl)

        if spl[-1] == "0":
            mesaj = "id:" + str(cli_data_next_count)
            userdata = re_id(spl, cli_data_next_count)
            cli_datas.append(userdata)
            cli_data_next_count += 1
            c.send(mesaj.encode("utf-8"))
        else:
            cli_datas[int(spl[-1])] = userdata
            c.send(re_message(cli_datas).encode("utf-8"))

        print(cli_datas)
        c.close()

    except socket.error as e:
        print("Connection error:", e)
        # Handle connection errors gracefully (e.g., log the error)
