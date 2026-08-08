import os
import random
import itertools
import threading
from flask import Flask
import telebot

# ----------------------------------------------------
# 1. TẠO WEB SERVER THU NHỎ (Để Render giữ bot 24/7)
# ----------------------------------------------------
app = Flask(__name__)


@app.route("/")
def home():
    return "Bot Telegram Baccarat đang hoạt động 24/7!"


def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ----------------------------------------------------
# 2. TỰ ĐỘNG TẠO 10.000+ CÂU GIAO LƯU (5-7 CHỮ)
# ----------------------------------------------------
def generate_gambling_sentences():
    prefix = [
        "Nay",
        "Hôm nay",
        "Ván này",
        "Tay này",
        "Ca này",
        "Cầu này",
        "Anh em",
        "Sếp ơi",
        "Giờ này",
        "Quả này",
        "Đêm nay",
        "Lượt này",
    ]
    action = [
        "theo",
        "chốt",
        "gõ",
        "giã",
        "bắt",
        "vào tiền",
        "phang",
        "đập",
        "đè",
        "kéo",
        "đánh",
        "xuống tiền",
    ]
    target = [
        "Banker hay Player",
        "cửa Nhà Cái",
        "cửa Con",
        "quả bệt này",
        "tay bẻ này",
        "kèo thơm này",
        "cầu đôi này",
        "cửa Hòa to",
        "dây đỏ này",
        "kèo xanh chín",
        "tay kết này",
        "cầu nghiêng này",
    ]
    suffix = [
        "không anh ơi",
        "có húp không",
        "về bờ chưa",
        "uy tín không",
        "được không sếp",
        "có thắng lớn",
        "ăn to không",
        "ngon lành không",
        "có bú không",
        "được không anh",
    ]

    sentences = set()
    for p, a, t, s in itertools.product(prefix, action, target, suffix):
        sentence = f"{p} {a} {t} {s}?"
        word_count = len(sentence.split())
        if 5 <= word_count <= 7:
            sentences.add(sentence)

    return list(sentences)


# Tải kho câu vào bộ nhớ
SENTENCES_POOL = generate_gambling_sentences()
print(f"Đã khởi tạo {len(SENTENCES_POOL)} câu Baccarat không trùng lặp!")

# ----------------------------------------------------
# 3. CẤU HÌNH VÀ XỬ LÝ LỆNH TELEGRAM BOT
# ----------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(
    func=lambda msg: msg.text and msg.text.strip().lower() == "o5"
)
def handle_o5(message):
    # Lấy ngẫu nhiên 10 câu không trùng lặp
    if len(SENTENCES_POOL) >= 10:
        selected = random.sample(SENTENCES_POOL, 10)
        reply_text = "\n".join(selected)
        bot.reply_to(message, reply_text)


if __name__ == "__main__":
    # Chạy Web Server ở luồng riêng
    threading.Thread(target=run_flask, daemon=True).start()

    print("Bot đã sẵn sàng nhận tin nhắn...")
    bot.infinity_polling()
  
