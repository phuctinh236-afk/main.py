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
# 2. KHO CÂU CHAT NGƯỜI CHƠI THỰC TẾ (BAO GỒM BÁO CỘNG TIỀN +2M, +3M)
# ----------------------------------------------------
RAW_PLAYER_CHAT = [
    # --- Nhóm Báo Ăn / Cộng Tiền (+2m, +3m, +5m...) ---
    "+2m húp rồi anh ơi",
    "+3m ấm no rồi sếp ơi",
    "Húp nhẹ 2m rồi sếp ơi",
    "+5m về bờ ngọt ngào luôn",
    "Lại cộng 2m ngon lành luôn",
    "Cộng 3m uy tín quá sếp",
    "Mới bú 2m ấm quá anh",
    "Ăn quả 3m ấm no luôn",
    "Húp gọn 2m rồi sếp ơi",
    "+2m húp trọn ván này rồi",
    "Bú 5m về bờ rồi anh",
    "+3m húp đậm rồi sếp ơi",
    "Mới húp 3m ngọt quá anh",
    "Lại bú 2m ngon lành luôn",
    "Cộng 5m về bờ luôn anh",
    "+2m ấm no ca này rồi",
    "Làm quả 3m ấm quá anh",
    "Ăn nhẹ 2m rồi sếp ơi",
    "+3m trọn ván rồi anh em",
    "Vừa cộng 2m ngọt ngào luôn",
    # --- Nhóm Báo Vốn & Đợi Live ---
    "Em vừa lên vốn xong rồi anh",
    "Vốn sẵn trong game rồi nha sếp",
    "Em nạp tiền rồi chờ lệnh thôi",
    "Sếp ơi nay kéo ca mấy giờ",
    "Lên live chưa idol ơi hóng quá",
    "Em chờ anh từ chiều tới giờ",
    "Đợi mãi mới thấy anh lên live",
    "Nay nạp vốn to theo sếp rồi",
    "Sẵn vốn rồi chiến thôi anh ơi",
    "Em nạp sẵn chờ sếp hô lệnh",
    "Sếp ơi nay đánh sảnh nào thế",
    "Nay quyết tâm vớt lại hôm qua",
    "Em sẵn sàng rồi chiến thôi anh",
    "Lên chưa anh ơi anh em đợi",
    "Đã lên tiền chờ sếp kéo nha",
    "Nạp xong vốn rồi nhé sếp ơi",
    # --- Nhóm Hỏi Kèo & Xin Góc Đánh ---
    "Tay này chốt Con hay Cái anh",
    "Tay này bệt Banker luôn không sếp",
    "Tay này bẻ cầu được chưa anh",
    "Làm quả bệt này uy tín không",
    "Ván này vào tiền thế nào anh",
    "Bắt quả cầu đôi này ngon luôn",
    "Ván này theo cửa nào vậy sếp",
    "Cầu 1 1 này bệt tiếp không",
    "Tay này nghiêng cửa nào hơn anh",
    "Chốt hạ tay này nghỉ luôn sếp",
    "Vừa vào tiền tay Con rồi anh",
    "Chờ lệnh sếp gõ ván này nè",
    "Em theo sếp ván này xanh chín",
    "Tay này vào mạnh được chưa anh",
    "Gõ tay này xong về bờ luôn",
    "Làm tay kết về bờ thôi sếp",
    "Chốt quả Cái này húp đậm không",
    # --- Nhóm Ăn To & Về Bờ ---
    "Húp ngọt quá sếp ơi uy tín",
    "Ăn đậm tay này rồi anh ơi",
    "Cảm ơn sếp ca này ấm quá",
    "Lại húp rồi uy tín quá anh",
    "Theo sếp đúng là về bờ ngay",
    "Dây đỏ lại rồi húp thông ca",
    "Cầu đi đẹp quá húp liên tục",
    "Ngon lành luôn sếp ơi đẳng cấp",
    "Quả cầu này nét quá sếp ơi",
    "Húp trọn ván này rồi anh em",
    "Húp đậm sâu luôn sếp ơi",
    "Bú trọn tay này rồi sếp ơi",
    "Đỉnh quá sếp ơi húp liên tục",
    "Bờ đây rồi cảm ơn sếp nha",
    "Ca này ấm no rồi anh em",
    "Sếp hô chuẩn quá húp miệt mài",
]

# Tự động lọc đảm bảo 100% câu từ 5 đến 7 chữ
ALL_SENTENCES = [
    s for s in RAW_PLAYER_CHAT if 5 <= len(s.strip().split()) <= 7
]

# Cơ chế xoay vòng chống lặp lại giữa các lần gõ o5
unused_sentences = []


def get_10_unique_sentences():
    global unused_sentences
    if len(unused_sentences) < 10:
        unused_sentences = ALL_SENTENCES.copy()
        random.shuffle(unused_sentences)

    selected = unused_sentences[:10]
    unused_sentences = unused_sentences[10:]
    return selected


# ----------------------------------------------------
# 3. CẤU HÌNH VÀ XỬ LÝ LỆNH TELEGRAM BOT
# ----------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(
    func=lambda msg: msg.text and msg.text.strip().lower() == "o5"
)
def handle_o5(message):
    selected_10 = get_10_unique_sentences()
    reply_text = "\n".join(selected_10)
    bot.reply_to(message, reply_text)


if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print(
        f"Bot đã khởi tạo thành công {len(ALL_SENTENCES)} câu chốt lời Baccarat!"
    )
    bot.infinity_polling()
    
