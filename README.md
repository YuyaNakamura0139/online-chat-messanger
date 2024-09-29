# online-chat-messanger

UDP通信を用いて、クライアント同士がメッセージをやり取りできるチャットメッセンジャーサービスを作成しました。

## 使用言語

Python

## 使い方

### 0. 準備

リポジトリをクローンしてください。

```zsh
$ git clone https://github.com/YuyaNakamura0139/online-chat-messanger.git
```

### 1. サーバーを起動

```zsh
$ python server/main.py
```

### 2. クライアントを起動してユーザー名を入力

ご自身のユーザー名を入力してください。

```zsh
$ python client/main.py
Enter your name: <ユーザー名>
```

###3. メッセージを入力して送信

お好きなメッセージを入力して送信してください。

```zsh
<メッセージ>
```

### 4. メッセージを受信

他のクライアントからメッセージを常に受信します。

```zsh
<ユーザー名>: <メッセージ>
```

デモ動画

![2024-09-300 32 58-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/049c86a7-fad8-4a3f-bce7-d4cdcb07e4a7)