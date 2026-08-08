import itertools
import os
import random
import threading
from flask import Flask
import telebot

# ----------------------------------------------------
# 1. WEB SERVER GIỮ BOT CHẠY 24/7 TRÊN RENDER
# ----------------------------------------------------
app = Flask(__name__)


@app.route("/")
def home():
    return "Bot Baccarat Live Stream đang chạy 24/7!"


def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ----------------------------------------------------
# 2. BỘ TẠO CÂU: CHỜ LIVE / LÊN VỐN / HÔ LỆNH ĂN TO (5-7 CHỮ)
# ----------------------------------------------------
def generate_live_stream_sentences():
    # Nhóm 1: Mẫu câu báo lên vốn & chờ lên live
    set1_prefix = [
        "Anh ơi",
        "Sếp ơi",
        "Idol ơi",
        "Anh em",
        "Em sẵn",
        "Đã nạp",
    ]
    set1_mid = [
        "lên live chưa",
        "lên vốn xong",
        "chờ từ sớm",
        "chuẩn bị tiền",
        "vào vốn sẵn",
        "đợi sếp hô",
    ]
    set1_suffix = [
        "chưa anh ơi?",
        "rồi nè anh!",
        "giờ rồi anh!",
        "chờ lệnh nhé!",
        "chiến thôi anh!",
        "rồi sếp ơi!",
    ]

    # Nhóm 2: Mẫu câu chốt kèo, đánh là ăn, về bờ
    set2_prefix = [
        "Ván này",
        "Tay này",
        "Quả này",
        "Cầu này",
        "Theo sếp",
        "Gõ tay",
    ]
    set2_mid = [
        "chốt hạ chắc",
        "giã mạnh tay",
        "xuống tiền là",
        "đánh cửa này",
        "vào tiền to",
        "theo kèo này",
    ]
    set2_suffix = [
        "ăn to anh!",
        "húp đậm luôn!",
        "về bờ ngay!",
        "ngon lành luôn!",
        "chắc thắng nhé!",
        "thắng lớn nha!",
    ]

    unique_sentences = set()

    # Sinh câu nhóm 1 (Báo vốn, chờ live)
    for p, m, s in itertools.product(set1_prefix, set1_mid, set1_suffix):
        sentence = f"{p} {m} {s}".strip()
        if 5 <= len(sentence.split()) <= 7:
            unique_sentences.add(sentence)

    # Sinh câu nhóm 2 (Hô lệnh, chốt ván ăn đậm)
    for p, m, s in itertools.product(set2_prefix, set2_mid, set2_suffix):
        sentence = f"{p} {m} {s}".strip()
        if 5 <= len(sentence.split()) <= 7:
            unique_sentences.add(sentence)

    return list(unique_sentences)


# Khởi tạo danh sách câu
SENTENCES_POOL = generate_live_stream_sentences()
print(f"Đã khởi tạo thành công {len(SENTENCES_POOL)} câu phong cách Live Stream!")

# ----------------------------------------------------
# 3. CẤU HÌNH VÀ XỬ LÝ LỆNH TELEGRAM BOT
# ----------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(
    func=lambda msg: msg.text and msg.text.strip().lower() == "o5"
)
def handle_o5(message):
    if len(SENTENCES_POOL) >= 10:
        selected = random.sample(SENTENCES_POOL, 10)
        reply_text = "\n".join(selected)
        bot.reply_to(message, reply_text)


if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot đã sẵn sàng nhận lệnh o5...")
    bot.infinity_polling()
    
