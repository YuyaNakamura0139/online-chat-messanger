import socket
import threading


class User:
    def __init__(self, user_name, ip_address, port):
        self.user_name = user_name
        self.ip_address = ip_address
        self.port = port


class UDPServer:
    def __init__(self):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_address = "0.0.0.0"
        self.server_port = 9003
        self.buffer_size = 4096
        self.user_map = {}
        self.message_queue = []
        self.running = True

    def sock_bind(self):
        self.sock.bind((self.server_address, self.server_port))

    def recv_data(self):
        try:
            while True:
                # client_address: (ip, port)
                data, client_address = self.sock.recvfrom(self.buffer_size)
                ip_address, port = client_address
                if data:
                    user_name, message = data.decode("utf-8").split(":")
                    user = User(user_name, ip_address, port)
                    self.user_map[user_name] = user
                    self.message_queue.append(
                        {
                            "user_name": user_name,
                            "ip_address": ip_address,
                            "port": port,
                            "message": message,
                        }
                    )
        except Exception as e:
            if self.running:
                print(e)

    def broadcast(self):
        try:
            while self.running:
                if len(self.message_queue) == 0:
                    continue
                message = self.message_queue[0]
                print(message)
                for user in self.user_map.values():
                    if user.user_name != message["user_name"]:
                        return_message = f"{message['user_name']}: {message['message']}"
                        self.sock.sendto(
                            return_message.encode("utf-8"), (user.ip_address, user.port)
                        )
                self.message_queue.pop(0)
        except Exception as e:
            if self.running:
                print(e)

    def close(self):
        self.running = False
        self.sock.close()

    def chat_start(self):
        self.sock_bind()
        recv = threading.Thread(target=self.recv_data)
        send = threading.Thread(target=self.broadcast)
        recv.start()
        send.start()
        try:
            recv.join()
            send.join()
        except KeyboardInterrupt:
            print("\n...Server down.")
        finally:
            self.close()


def main():
    server = UDPServer()
    server.chat_start()


if __name__ == "__main__":
    main()
