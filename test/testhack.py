# كود لإنشاء ملف وهمي يمثل "اللعبة"
def create_dummy_game():
    # بنكتب بايتس بتمثل كود اللعبة
    # السطر ده معناه: "Game code running..."
    content = b"\x47\x61\x6d\x65\x20\x63\x6f\x64\x65\x20\x72\x75\x6e\x6e\x69\x6e\x67\x2e\x2e\x2e"
    with open("game.bin", "wb") as f:
        f.write(content)
    print("تم إنشاء ملف اللعبة: game.bin")


create_dummy_game()
