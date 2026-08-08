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
    return "Bot Telegram Baccarat đang chạy 24/7!"


def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ----------------------------------------------------
# 2. DANH SÁCH CÂU CHAT NGƯỜI CHƠI THỰC TẾ (5-7 CHỮ)
# ----------------------------------------------------
# Dùng danh sách câu tự nhiên trực tiếp thay vì ghép từ tự động
REAL_PLAYER_CHAT = [
    # Báo vốn / Hóng live / Đợi kèo
    "Em lên vốn xong rồi nè anh",
    "Sếp ơi nay kéo ca mấy giờ",
    "Lên live chưa idol ơi hóng quá",
    "Em đợi anh từ chiều tới giờ",
    "Vốn sẵn trong game rồi nha sếp",
    "Đợi mãi mới thấy anh lên live",
    "Nay chuẩn bị vốn to theo anh",
    "Chờ lệnh sếp hô là phang liền",
    "Hôm nay có kéo ca đêm không",
    "Em vào vốn rồi chờ sếp hô",
    "Sếp ơi nay đánh bên sảnh nào",
    "Nay vớt lại ca hôm qua nha",
    "Em sẵn sàng rồi chiến thôi anh",
    "Lên chưa anh ơi anh em đợi",
    # Hỏi kèo / Hô lệnh / Đánh bài
    "Tay này bệt Banker luôn không sếp",
    "Tay này chốt Con hay Cái anh",
    "Làm quả bẻ cầu uy tín đi",
    "Chốt ván này húp đậm luôn anh",
    "Vừa vào tiền tay Con rồi anh",
    "Chờ lệnh sếp gõ ván này nè",
    "Em theo sếp ván này xanh chín",
    "Tay này vào mạnh được chưa anh",
    "Bắt quả cầu đôi này ngon luôn",
    "Anh ơi ván này đánh cửa nào",
    "Gõ tay này xong về bờ luôn",
    "Làm tay kết về bờ thôi sếp",
    "Vào đúng cầu ngon rồi anh ơi",
    "Cầu 1 1 này bệt tiếp không",
    "Tay này nghiêng về cửa nào anh",
    "Chốt hạ tay này nghỉ luôn sếp",
    # Ăn to / Về bờ / Cảm ơn sếp
    "Húp ngọt quá sếp ơi uy tín",
    "Ăn đậm tay này rồi anh ơi",
    "Theo sếp đúng là về bờ ngay",
    "Cầu đi đẹp quá húp liên tục",
    "Ngon lành luôn sếp ơi đẳng cấp",
    "Lại ăn rồi uy tín quá anh",
    "Dây đỏ lại rồi húp thông ca",
    "Quả cầu này nét quá sếp ơi",
    "Húp trọn ván này rồi anh em",
    "Cảm ơn sếp ca này ấm quá",
]


# Lọc lại để đảm bảo 100% câu từ 5 đến 7 chữ
def get_valid_sentences():
    valid_list = []
    for sentence in REAL_PLAYER_CHAT:
        words = sentence.strip().split()
        if 5 <= len(words) <= 7:
            valid_list.append(sentence)
    return valid_list


SENTENCES_POOL = get_valid_sentences()
print(f"Đã tải {len(SENTENCES_POOL)} câu chat người chơi thực tế!")

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
        # Lấy ngẫu nhiên 10 câu không lặp lại
        selected = random.sample(SENTENCES_POOL, 10)
        reply_text = "\n".join(selected)
        bot.reply_to(message, reply_text)


if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot đã sẵn sàng nhận lệnh o5...")
    bot.infinity_polling()
