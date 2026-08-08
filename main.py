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
# 2. KHO CÂU CHAT NGƯỜI CHƠI THỰC TẾ (CHUẨN 5-7 CHỮ)
# ----------------------------------------------------
RAW_PLAYER_CHAT = [
    # --- Nhóm 1: Báo vốn & Đợi live ---
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
    "Báo danh ca đêm chờ sếp hô",
    "Nạp xong vốn rồi nhé sếp ơi",
    "Hóng sếp lên live từ sáng giờ",
    "Chờ lệnh sếp phang ván này nha",
    "Hôm nay có ca kéo đêm không",
    # --- Nhóm 2: Hỏi kèo & Xin góc đánh ---
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
    "Ván này đánh cửa nào vậy sếp",
    "Gõ tay này xong về bờ luôn",
    "Làm tay kết về bờ thôi sếp",
    "Vào đúng cầu ngon rồi anh ơi",
    "Chốt quả Cái này húp đậm không",
    "Có nên bẻ quả cầu này không",
    "Ván này vào tiền nhẹ tay thôi",
    "Kèo này chắc ăn không sếp ơi",
    "Bắt quả cầu bệt này ngon đét",
    "Tay này đánh cửa Con ngon không",
    # --- Nhóm 3: Ăn to / Húp đậm / Về bờ ---
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
    "Lại ăn rồi đẳng cấp quá anh",
    "Vỡ hũ ca này rồi anh em",
    "Húp đậm sâu luôn sếp ơi",
    "Chốt ca này ấm no rồi anh",
    "Bú trọn tay này rồi sếp ơi",
    "Ấm no ca này rồi sếp ơi",
    "Đỉnh quá sếp ơi húp liên tục",
    "Tay này ăn đậm luôn rồi anh",
    "Bờ đây rồi cảm ơn sếp nha",
    "Làm quả húp ngọt xơ rơ luôn",
    "Ca này ấm no rồi anh em",
    "Sếp hô chuẩn quá húp miệt mài",
    # --- Nhóm 4: Tâm lý & Xin kéo gỡ ---
    "Ca này quyết tâm về bờ nha",
    "Gỡ lại ca hôm qua thôi anh",
    "Kéo em về bờ với sếp ơi",
    "Nay em đang xui kéo em với",
    "Ca này mong gỡ lại tí vốn",
    "Tay này vào vừa tiền thôi anh",
    "Giữ cái đầu lạnh chơi tiếp nha",
    "Đánh cẩn thận tay này nha anh",
    "Theo sếp từ đầu tuần tới giờ",
    "Vừa vào dây đỏ húp đậm luôn",
    "Mong ca này gỡ lại tiền vốn",
    "Sếp kéo em về bờ với nha",
    "Nay phải lấy lại những gì mất",
    "Cố gắng ca này gỡ lại vốn",
    # --- Nhóm 5: Tự nhiên chém gió trong livestream ---
    "Anh em nay thắng lớn không thế",
    "Hôm nay sếp kéo nét quá chừng",
    "Mọi người nay ăn to không vậy",
    "Cầu đẹp thế này đánh sướng tay",
    "Nhìn cầu này là muốn xuống tiền",
    "Chờ mãi mới gặp được dây đỏ",
    "Nay theo sếp bú ngập răng luôn",
    "Cầu này đi dài quá anh em",
    "Càng đánh càng mê sếp ơi",
    "Nay ai cũng về bờ hết rồi",
]

# Lọc tự động đảm bảo 100% câu từ 5 đến 7 chữ
ALL_SENTENCES = [
    s for s in RAW_PLAYER_CHAT if 5 <= len(s.strip().split()) <= 7
]

# Cơ chế hàng đợi chống trùng lặp qua các lần nhắn o5
unused_sentences = []


def get_10_unique_sentences():
    global unused_sentences
    # Nếu kho chưa dùng còn dưới 10 câu, xáo trộn lại toàn bộ kho
    if len(unused_sentences) < 10:
        unused_sentences = ALL_SENTENCES.copy()
        random.shuffle(unused_sentences)

    # Lấy 10 câu chưa từng xuất hiện ra
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
    print(f"Bot đã khởi tạo thành công {len(ALL_SENTENCES)} câu khác nhau!")
    bot.infinity_polling()
    
