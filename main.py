import html
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
# 2. KHO CÂU CHAT NGƯỜI CHƠI THỰC TẾ (5-7 CHỮ)
# ----------------------------------------------------
RAW_PLAYER_CHAT = [
    # --- Nhóm 1: Báo CỘNG TIỀN / Thắng Lớn ---
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
    "+1m húp nhẹ ván này nha",
    "+5m ấm no quá anh ơi",
    "Lụm 2m gọn gàng rồi anh",
    "+10m về bờ an toàn rồi",
    "Bú 3m ngọt xơ rơ luôn",
    "+2m húp ấm quá sếp ơi",
    "Lụm nhẹ 3m rồi anh em",
    "Cộng 500k nhẹ nhàng rồi anh",
    "+500k húp gọn ván này nha",
    "+1m ấm no ca này rồi",
    "Bú 2m nhẹ nhàng quá anh",
    "+3m về bờ an toàn rồi",
    "Lụm 5m ngọt ngào quá sếp",
    "+2m vào tài khoản rồi anh",
    "Húp 3m ấm cúng quá sếp",
    "+5m bú trọn ván này rồi",
    "Cộng 2m nhẹ nhàng quá sếp",
    "+3m húp trọn ván này nha",
    "Lụm 2m ngọt lịm rồi anh",
    "+1m nhẹ nhàng húp rồi anh",
    # --- Nhóm 2: Báo Vốn / Nạp Tiền / Đợi Live Stream ---
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
    "Em mới nạp xong 5m rồi",
    "Lên vốn 2m sẵn sàng rồi",
    "Em đã nạp vốn chờ sếp",
    "Vốn 3m sẵn sàng chiến rồi",
    "Sếp ơi em sẵn vốn rồi",
    "Lên tiền sẵn chờ sếp hô",
    "Đã vào vốn chờ sếp kéo",
    "Hôm nay quyết tâm gỡ vốn",
    "Sẵn sàng nạp thêm vốn rồi",
    "Đã chuẩn bị vốn to rồi",
    "Vốn nạp sẵn sàng rồi sếp",
    "Em chuẩn bị xong tiền rồi",
    "Nay vào vốn to theo sếp",
    "Sếp ơi em lên tiền rồi",
    # --- Nhóm 3: Hỏi Kèo / Bệt / Bẻ ---
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
    "Tay này nghiêng Con hơn đúng không",
    "Cầu bệt 4 tay rồi sếp",
    "Có nên bẻ quả cầu này",
    "Tay này chốt cửa Con nha",
    "Vào tiền ván này thế nào",
    "Bắt cầu 1 1 ngon không",
    "Cầu này nên bệt hay bẻ",
    "Ván này gõ mạnh được chưa",
    "Theo Cái ván này được không",
    "Nên vào tiền tay này không",
    "Ván này chốt cửa nào sếp",
    "Bệt tiếp Banker được không anh",
    "Bẻ cầu Player ván này nha",
    "Tay này kết cửa Con quá",
    "Cầu đi đẹp quá sếp ơi",
    "Quả cầu 2 2 đẹp đẽ",
    "Kèo này uy tín không sếp",
    "Nên chốt Con hay Cái anh",
    # --- Nhóm 4: Hô Húp / Báo Về Bờ ---
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
    "Uy tín quá sếp ơi húp",
    "Húp tràn màn hình luôn anh",
    "Ăn đậm ca này rồi sếp",
    "Bú ngập răng rồi sếp ơi",
    "Đại thắng ca này rồi anh",
    "Cảm ơn sếp kéo em về",
    "Ca này ấm lòng quá sếp",
    "Về bờ thành công rồi anh",
    "Thắng lớn ca này rồi sếp",
    "Quá đẳng cấp sếp ơi húp",
    "Đánh theo sếp chỉ có thắng",
    "Ca này húp đẫm rồi anh",
    "Bú thông 5 tay rồi sếp",
    "Đúng là idol kéo có khác",
]

# Tự động lọc đảm bảo 100% câu từ 5 đến 7 chữ
ALL_SENTENCES = [
    s for s in RAW_PLAYER_CHAT if 5 <= len(s.strip().split()) <= 7
]

# Cơ chế xoay vòng chống trùng lặp
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
# 3. CẤU HÌNH VÀ TẠO MENU CHẠM LÀ COPY (PARSER HTML)
# ----------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(
    func=lambda msg: msg.text and msg.text.strip().lower() == "o5"
)
def handle_o5(message):
    selected_10 = get_10_unique_sentences()

    # Dựng giao diện Tool / Game (Termux Style)
    lines = []
    lines.append("<b>[ - BACCARAT TOOL VIP - ]</b>")
    lines.append("<code>═════════════════════════════════════</code>")
    lines.append("<code>~{ }~ Status: Active | Mode: Auto O5</code>")
    lines.append("<code>[NQ-TOOL] | User: VIP | Status: SUCCESS</code>")
    lines.append("<code>─────────────────────────────────────</code>")

    # Mỗi câu được bọc trong thẻ <code> giúp bấm nhẹ vào câu đó là COPY tự động
    for idx, sentence in enumerate(selected_10, 1):
        escaped_s = html.escape(sentence)
        lines.append(f"[{idx:02d}] <code>{escaped_s}</code>")

    lines.append("<code>─────────────────────────────────────</code>")
    lines.append("<code>~{ }~ Dùng Tool Vui Vẻ! Gõ O5 Lấy Tiếp</code>")
    lines.append("<code>═════════════════════════════════════</code>")

    reply_text = "\n".join(lines)

    try:
        # Gửi tin nhắn chế độ HTML
        bot.reply_to(message, reply_text, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, "\n".join(selected_10))


if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot đã sẵn sàng với Menu Tool COPY 1-Chạm!")
    bot.infinity_polling()
