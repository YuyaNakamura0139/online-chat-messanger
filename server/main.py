import json
import socket
from request import RequestHandler


# UDP Socket
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

server_address = "0.0.0.0"
server_port = 9002
sock.bind((server_address, server_port))


def main():
    print(f"Starting up on {server_address} port {server_port}")

    try:
        while True:
            # Receive data from client.
            # 4096 is the buffer size.
            data, client_address = sock.recvfrom(4096)
            if data:
                json_data = json.loads(data.decode("utf-8"))
                print(json_data)
                handler = RequestHandler(request=json_data)
                response = handler.handle_request()
                sock.sendto(json.dumps(response).encode("utf-8"), client_address)
    finally:
        sock.close()


if __name__ == "__main__":
    main()
