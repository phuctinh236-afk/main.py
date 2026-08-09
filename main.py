import html
import os
import random
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# ----------------------------------------------------
# 1. WEB SERVER GIỮ BOT CHẠY 24/7 TRÊN RENDER
# ----------------------------------------------------
app = Flask(__name__)


@app.route("/")
def home():
    return "Mini Game Baccarat Tool Bot đang chạy 24/7!"


def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ----------------------------------------------------
# 2. BOT TELEGRAM & DỮ LIỆU MINI GAME
# ----------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Lưu trữ dữ liệu người chơi trong bộ nhớ (Xu, Thắng, Thua)
user_data = {}


def get_user(user_id, name):
    if user_id not in user_data:
        user_data[user_id] = {
            "name": name,
            "xu": 10000,  # Tặng 10,000 Xu khởi tạo
            "wins": 0,
            "losses": 0,
        }
    return user_data[user_id]


# Kho 100+ câu chat người chơi (5-7 chữ)
RAW_PLAYER_CHAT = [
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
    "Em vừa lên vốn xong rồi anh",
    "Vốn sẵn trong game rồi nha sếp",
    "Em nạp tiền rồi chờ lệnh thôi",
    "Sếp ơi nay kéo ca mấy giờ",
    "Lên live chưa idol ơi hóng quá",
    "Tay này chốt Con hay Cái anh",
    "Tay này bệt Banker luôn không sếp",
    "Tay này bẻ cầu được chưa anh",
    "Húp ngọt quá sếp ơi uy tín",
    "Ăn đậm tay này rồi anh ơi",
    "Cảm ơn sếp ca này ấm quá",
    "Lại húp rồi uy tín quá anh",
    "Theo sếp đúng là về bờ ngay",
]

ALL_SENTENCES = [
    s for s in RAW_PLAYER_CHAT if 5 <= len(s.strip().split()) <= 7
]


# ----------------------------------------------------
# 3. GIAO DIỆN MENU HACKER / TERMINAL (LIKE IMAGE)
# ----------------------------------------------------
def create_main_menu(user_info):
    text = (
        f"<b>[ - BACCARAT TOOL MINI GAME - ]</b>\n"
        f"<code>═════════════════════════════════════</code>\n"
        f"<code>~{{ }}~ Status: ONLINE | Mode: Interactive</code>\n"
        f"<code>[NQ-TOOL] | User: {user_info['name'][:12]} | Xu: {user_info['xu']:,}</code>\n"
        f"<code>─────────────────────────────────────</code>\n"
        f"<code>[1] 🎲 Chơi Baccarat (Đặt Cược)</code>\n"
        f"<code>[2] 💬 Lấy 10 Câu Chat (Copy 1-Chạm)</code>\n"
        f"<code>[3] 🎁 Điểm Danh Nhận +5,000 Xu</code>\n"
        f"<code>[4] 👤 Xem Hồ Sơ & Lịch Sử Thắng/Thua</code>\n"
        f"<code>─────────────────────────────────────</code>\n"
        f"<code>~{{ }}~ Nhấp nút bên dưới hoặc gõ số [1-4]</code>\n"
        f"<code>═════════════════════════════════════</code>"
    )

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🎲 [1] Chơi Game", callback_data="btn_game"),
        InlineKeyboardButton("💬 [2] Copy Chat", callback_data="btn_chat"),
    )
    markup.row(
        InlineKeyboardButton("🎁 [3] Điểm Danh", callback_data="btn_daily"),
        InlineKeyboardButton("👤 [4] Hồ Sơ", callback_data="btn_profile"),
    )
    return text, markup


# ----------------------------------------------------
# 4. HANDLERS LỆNH & TIN NHẮN
# ----------------------------------------------------
@bot.message_handler(commands=["start", "menu"])
@bot.message_handler(
    func=lambda msg: msg.text and msg.text.strip().lower() in ["menu", "o5"]
)
def show_menu(message):
    user = get_user(message.from_user.id, message.from_user.first_name)

    # Nếu người dùng gõ trực tiếp O5 -> Trả về danh sách copy ngay lập tức
    if message.text and message.text.strip().lower() == "o5":
        send_copy_sentences(message.chat.id)
        return

    text, markup = create_main_menu(user)
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text in ["1", "2", "3", "4"])
def handle_number_input(message):
    user = get_user(message.from_user.id, message.from_user.first_name)
    choice = message.text.strip()

    if choice == "1":
        send_baccarat_game(message.chat.id, user)
    elif choice == "2":
        send_copy_sentences(message.chat.id)
    elif choice == "3":
        claim_daily_xu(message.chat.id, user)
    elif choice == "4":
        send_profile_info(message.chat.id, user)


# ----------------------------------------------------
# 5. XỬ LÝ SỰ KIỆN NÚT BẤM (CALLBACK)
# ----------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user = get_user(call.from_user.id, call.from_user.first_name)

    if call.data == "btn_game":
        send_baccarat_game(call.message.chat.id, user)
    elif call.data == "btn_chat":
        send_copy_sentences(call.message.chat.id)
    elif call.data == "btn_daily":
        claim_daily_xu(call.message.chat.id, user)
    elif call.data == "btn_profile":
        send_profile_info(call.message.chat.id, user)
    elif call.data in ["bet_player", "bet_banker"]:
        play_baccarat_round(call.message.chat.id, user, call.data)
    elif call.data == "btn_back_menu":
        text, markup = create_main_menu(user)
        bot.send_message(
            call.message.chat.id, text, parse_mode="HTML", reply_markup=markup
        )

    bot.answer_callback_query(call.id)


# ----------------------------------------------------
# 6. CÁC HÀM TÍNH NĂNG CON
# ----------------------------------------------------
def send_copy_sentences(chat_id):
    selected = random.sample(ALL_SENTENCES, min(10, len(ALL_SENTENCES)))
    lines = [
        "<b>[ - BACCARAT CHAT VIP - ]</b>",
        "<code>═════════════════════════════════════</code>",
        "<code>~{ }~ Chạm nhẹ vào câu để COPY tự động</code>",
        "<code>─────────────────────────────────────</code>",
    ]
    for idx, s in enumerate(selected, 1):
        lines.append(f"[{idx:02d}] <code>{html.escape(s)}</code>")

    lines.append("<code>─────────────────────────────────────</code>")
    lines.append("<code>~{ }~ Gõ O5 hoặc 2 để lấy danh sách mới</code>")
    lines.append("<code>═════════════════════════════════════</code>")

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔙 Về Menu Chính", callback_data="btn_back_menu")
    )
    bot.send_message(
        chat_id, "\n".join(lines), parse_mode="HTML", reply_markup=markup
    )


def send_baccarat_game(chat_id, user):
    text = (
        f"<b>[ - MINI GAME BACCARAT - ]</b>\n"
        f"<code>═════════════════════════════════════</code>\n"
        f"<code>[NQ-TOOL] | Số Xu hiện có: {user['xu']:,} Xu</code>\n"
        f"<code>Mức cược mặc định: 1,000 Xu / Tay</code>\n"
        f"<code>─────────────────────────────────────</code>\n"
        f"<code>Vui lòng chọn cửa đặt cược bên dưới:</code>"
    )
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔵 Player (Con)", callback_data="bet_player"),
        InlineKeyboardButton("🔴 Banker (Cái)", callback_data="bet_banker"),
    )
    markup.add(
        InlineKeyboardButton("🔙 Về Menu Chính", callback_data="btn_back_menu")
    )
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)


def play_baccarat_round(chat_id, user, choice):
    bet_amount = 1000
    if user["xu"] < bet_amount:
        bot.send_message(
            chat_id,
            "<code>[NQ-TOOL] | Lỗi: Không đủ Xu! Vui lòng Điểm danh [3] để nhận thêm Xu.</code>",
            parse_mode="HTML",
        )
        return

    player_score = random.randint(0, 9)
    banker_score = random.randint(0, 9)

    winner = (
        "bet_player"
        if player_score > banker_score
        else ("bet_banker" if banker_score > player_score else "tie")
    )

    if winner == choice:
        user["xu"] += bet_amount
        user["wins"] += 1
        status = f"THẮNG! +{bet_amount:,} Xu"
    elif winner == "tie":
        status = "HÒA! Hoàn tiền cược"
    else:
        user["xu"] -= bet_amount
        user["losses"] += 1
        status = f"THUA! -{bet_amount:,} Xu"

    chosen_name = "🔵 Player (Con)" if choice == "bet_player" else "🔴 Banker (Cái)"

    res_text = (
        f"<b>[ - BACCARAT RESULT - ]</b>\n"
        f"<code>═════════════════════════════════════</code>\n"
        f"<code>[NQ-TOOL] | Analyzing card... SUCCESS!</code>\n"
        f"<code>Cửa bạn chọn: {chosen_name}</code>\n"
        f"<code>─────────────────────────────────────</code>\n"
        f"<code>🔵 Player: {player_score} Nút  |  🔴 Banker: {banker_score} Nút</code>\n"
        f"<code>─────────────────────────────────────</code>\n"
        f"<code>Kết quả: {status}</code>\n"
        f"<code>Số Xu còn lại: {user['xu']:,} Xu</code>\n"
        f"<code>═════════════════════════════════════</code>"
    )

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🎲 Đánh Ván Mới", callback_data="btn_game"),
        InlineKeyboardButton("🔙 Menu Chính", callback_data="btn_back_menu"),
    )
    bot.send_message(chat_id, res_text, parse_mode="HTML", reply_markup=markup)


def claim_daily_xu(chat_id, user):
    user["xu"] += 5000
    msg = (
        f"<b>[ - ĐIỂM DANH THÀNH CÔNG - ]</b>\n"
        f"<code>[NQ-TOOL] | +5,000 Xu đã được thêm vào tài khoản!</code>\n"
        f"<code>Tổng Xu hiện tại: {user['xu']:,} Xu</code>"
    )
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔙 Về Menu Chính", callback_data="btn_back_menu")
    )
    bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=markup)


def send_profile_info(chat_id, user):
    total_games = user["wins"] + user["losses"]
    win_rate = (
        (user["wins"] / total_games * 100) if total_games > 0 else 0.0
    )

    msg = (
        f"<b>[ - HỒ SƠ NGƯỜI CHƠI - ]</b>\n"
        f"<code>═════════════════════════════════════</code>\n"
        f"<code>Tên: {user['name']}</code>\n"
        f"<code>Số Xu: {user['xu']:,} Xu</code>\n"
        f"<code>Thắng: {user['wins']} ván  |  Thua: {user['losses']} ván</code>\n"
        f"<code>Tỷ lệ thắng: {win_rate:.1f}%</code>\n"
        f"<code>═════════════════════════════════════</code>"
    )
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔙 Về Menu Chính", callback_data="btn_back_menu")
    )
    bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=markup)


# ----------------------------------------------------
# 7. CHẠY BOT DÒNG LỆNH
# ----------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot Mini Game & Tool đã sẵn sàng!")
    bot.infinity_polling()
        
