import socket
import json
from typing import Dict, Any

# method: register_user, send_message_to_all_users


def register_user(user_name: str, address: str, port: int) -> Dict[str, Any]:
    request = {
        "method_name": "register_user",
        "params": {"user_name": user_name, "address": address, "port": port},
        "param_types": {
            "user_name": type(user_name).__name__,
            "address": type(address).__name__,
            "port": type(port).__name__,
        },
    }
    return request


sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Server address and port
server_address = "0.0.0.0"
server_port = 9002

# Client address and port
address = "0.0.0.0"
port = 9051

sock.bind((address, port))

print("Chat started.")

if __name__ == "__main__":
    try:
        # 初回のみユーザー登録
        # 3回ユーザー登録を間違えたら強制終了
        user_register_count = 0
        while True:
            user_name = input("Please enter your user name: ")
            request = register_user(user_name, address, port)
            sock.sendto(
                json.dumps(request).encode("utf-8"),
                (server_address, server_port),
            )
            data, server = sock.recvfrom(4096)
            response = json.loads(data.decode("utf-8"))
            if user_register_count == 3:
                print("Failed to register user.\nPlease try again later.")
                exit()
            elif response.get("message"):
                print("Success user registration.")
                break
            elif not response.get("message"):
                print("This user name is already used.")
                user_register_count += 1
                print(user_register_count)
                continue
        # チャットの開始
        while True:
            # Send data to server
            message = input(f"{user_name}: ")
            if message.lower() == "exit":
                break
            # Return the number of bytes sent
            sock.sendto(message.encode("utf-8"), (server_address, server_port))
            data, server = sock.recvfrom(4096)
            print(f"server: {data.decode('utf-8')}")
    except Exception as e:
        print(e)
    finally:
        print("Chat ended.")
        sock.close()
