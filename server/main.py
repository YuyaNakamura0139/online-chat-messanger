from datetime import datetime
import socket
import threading
import time


class User:
    """
    ユーザークラス
    """

    def __init__(self, user_name, ip_address, port):
        self.user_name = user_name
        self.ip_address = ip_address
        self.port = port
        self.updated_at = datetime.now()


class UDPServer:
    """
    UDPサーバークラス
    """

    def __init__(self):
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_address = "0.0.0.0"
        self.server_port = 9000
        self.buffer_size = 4096
        self.user_map = {}
        self.message_queue = []
        self.running = False  # サーバーが実行中かどうかのフラグ

    def sock_bind(self):
        """
        ソケットをバインドする
        """

        self.sock.bind((self.server_address, self.server_port))

    def recv_data(self):
        """
        データを受信する
        """

        try:
            while True:
                # client_address: (ip, port)
                data, client_address = self.sock.recvfrom(self.buffer_size)
                ip_address, port = client_address
                if data:
                    user_name, message = data.decode("utf-8").split(":")
                    print(f"{user_name}: {message}")
                    # ユーザーが存在する場合は更新日時を更新
                    if user_name in self.user_map:
                        self.user_map[user_name].updated_at = datetime.now()
                    # ユーザーが存在しない場合は新規作成
                    else:
                        user = User(user_name, ip_address, port)
                        self.user_map[user_name] = user
                    # メッセージキューに追加
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
        """
        ユーザーからのメッセージを他のユーザーへブロードキャストする
        """

        try:
            while self.running:
                if len(self.message_queue) == 0:
                    continue
                message = self.message_queue[0]
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
        """
        ソケットを閉じる
        """

        self.running = False
        self.sock.close()

    def check_user_timeout(self):
        """
        一定時間経過したユーザーを削除する。
        """
        while self.running:
            for user_name, user in list(self.user_map.items()):
                if (datetime.now() - user.updated_at).total_seconds() / 60 > 30:
                    del self.user_map[user_name]
                    print(f"{user_name}がタイムアウトにより削除されました。")

            # 5分おきに実行
            time.sleep(300)

    def chat_start(self):
        """
        チャットを開始する
        """

        print("...Server start.")
        self.sock_bind()
        self.running = True
        recv = threading.Thread(target=self.recv_data, daemon=True)
        send = threading.Thread(target=self.broadcast, daemon=True)
        check_timeout = threading.Thread(target=self.check_user_timeout, daemon=True)
        recv.start()
        send.start()
        check_timeout.start()
        try:
            recv.join()
            send.join()
            check_timeout.join()
        except KeyboardInterrupt:
            print("\n...Server down.")
        finally:
            self.close()


def main():
    server = UDPServer()
    server.chat_start()


if __name__ == "__main__":
    main()
