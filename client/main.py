import socket
import threading
import random


class UDPClient:
    def __init__(self):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.client_address = "127.0.0.1"
        self.client_port = random.randint(
            10000, 65535
        )  # クライアントのポート番号はランダムに設定
        self.buffer_size = 4096
        self.server_address = "127.0.0.1"
        self.server_port = 9000
        self.running = True

    def sock_bind(self) -> None:
        """
        ソケットをバインドする。
        もしバインドに失敗したら、ポート番号をランダムに変更して再度バインドする。
        """

        while True:
            try:
                self.sock.bind((self.client_address, self.client_port))
                break
            except OSError:
                self.client_port = random.randint(10000, 65535)

    def send_data(self, data) -> None:
        """
        データをサーバーに送信する。
        """

        try:
            self.sock.sendto(data, (self.server_address, self.server_port))
        except Exception as e:
            print(e)

    def recv_data(self) -> None:
        """
        サーバーからデータを受信し、標準出力する。
        """

        try:
            while True:
                data, client_address = self.sock.recvfrom(self.buffer_size)
                print(data.decode("utf-8"))
        except Exception as e:
            if self.running:
                print(e)

    def close(self) -> None:
        """
        ソケットを閉じる。
        """

        self.running = False
        self.sock.close()

    def send(self) -> None:
        """
        ユーザー名を入力し、データをサーバーに送信する。
        """

        user_name = input("Enter your name: ")
        try:
            while self.running:
                message = input()
                self.send_data(f"{user_name}:{message}".encode("utf-8"))
        except Exception as e:
            if self.running:
                print(e)

    def chat_start(self) -> None:
        """
        チャットを開始する。
        """

        self.sock_bind()
        send = threading.Thread(target=self.send)
        recv = threading.Thread(target=self.recv_data)
        send.start()
        recv.start()
        try:
            send.join()
            recv.join()
        except KeyboardInterrupt:
            print("\n...Close chat.")
        finally:
            self.close()


def main():
    client = UDPClient()
    try:
        print("...Client start")
        client.chat_start()
    except Exception as e:
        print(e)
    finally:
        client.close()


if __name__ == "__main__":
    main()
