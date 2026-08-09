import html
import os
import random
import threading
from flask import Flask, render_template_string
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# ----------------------------------------------------
# 1. KHO CÂU CHAT BACCARAT (5-7 CHỮ)
# ----------------------------------------------------
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
# 2. FLASK WEBAPP - GIAO DIỆN SẢNH TERMINAL ĐEN
# ----------------------------------------------------
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TX68 TERMINAL LOBBY</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { box-sizing: border-box; }
        body {
            background-color: #0c0d0e;
            color: #00ff66;
            font-family: 'Consolas', 'Courier New', monospace;
            padding: 10px;
            margin: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }
        .header {
            font-size: 10px;
            white-space: pre;
            color: #00e5ff;
            text-align: center;
            line-height: 1.1;
            margin-bottom: 8px;
            user-select: none;
        }
        .status-bar {
            background: #141619;
            border: 1px solid #22252a;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 11px;
            color: #888;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }
        .status-bar span { color: #00ff66; font-weight: bold; }
        
        /* KHUNG TERMINAL LOG CHÁT */
        .terminal-window {
            flex: 1;
            background: #050505;
            border: 1px solid #00ff66;
            border-radius: 4px;
            padding: 10px;
            overflow-y: auto;
            font-size: 12px;
            line-height: 1.5;
            box-shadow: inset 0 0 10px rgba(0, 255, 102, 0.1);
        }
        .log-line {
            margin-bottom: 4px;
            word-break: break-word;
        }
        .log-sys { color: #888; }
        .log-user { color: #00e5ff; }
        .log-bot { color: #00ff66; }
        .log-chat {
            background: #111;
            border-left: 3px solid #00ff66;
            padding: 4px 8px;
            margin: 4px 0;
            color: #fff;
            cursor: pointer;
            border-radius: 2px;
        }
        .log-chat:active {
            background: #00ff66;
            color: #000;
        }

        /* KHUNG NHẬP LỆNH CHÁT THỦ CÔNG */
        .input-box {
            display: flex;
            gap: 6px;
            margin-top: 8px;
            background: #141619;
            padding: 6px;
            border: 1px solid #333;
            border-radius: 4px;
        }
        .prompt-symbol {
            color: #00e5ff;
            font-weight: bold;
            line-height: 32px;
            padding-left: 4px;
        }
        input[type="text"] {
            flex: 1;
            background: transparent;
            border: none;
            color: #fff;
            font-family: inherit;
            font-size: 13px;
            outline: none;
        }
        .btn-send {
            background: #00ff66;
            color: #000;
            border: none;
            padding: 0 14px;
            font-family: inherit;
            font-weight: bold;
            cursor: pointer;
            border-radius: 3px;
        }

        /* NÚT TƯƠNG TÁC NHANH */
        .quick-actions {
            display: flex;
            gap: 6px;
            margin-top: 8px;
        }
        .btn-action {
            flex: 1;
            background: #181a1f;
            color: #00e5ff;
            border: 1px solid #00e5ff;
            padding: 8px 0;
            font-family: inherit;
            font-size: 11px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 3px;
            text-align: center;
        }
        .btn-action:active {
            background: #00e5ff;
            color: #000;
        }

        .toast {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #00ff66;
            color: #000;
            padding: 6px 16px;
            font-weight: bold;
            border-radius: 20px;
            display: none;
            box-shadow: 0 0 10px #00ff66;
            z-index: 999;
        }
    </style>
</head>
<body>

    <div class="header">
   ___ ____  _  _    ____ ____ _  _ ____ 
  |_  |__  || || |  |  __|  __| || |  __|
  |  _|  | || || |_ |  __|  __| || |  __|
  |___|  |_||__   _||____|____|____|____|
    </div>

    <div class="status-bar">
        <div>STATUS: <span>ACTIVE</span></div>
        <div>SERVER: <span>RENDER_NODE_01</span></div>
    </div>

    <!-- MÀN HÌNH TERMINAL CHÁT -->
    <div class="terminal-window" id="terminal">
        <div class="log-line log-sys">20:21:30 INCOMING HTTP REQUEST DETECTED ...</div>
        <div class="log-line log-sys">20:21:33 SERVICE WAKING UP ...</div>
        <div class="log-line log-bot">[SYSTEM] Sảnh Terminal TX68 đã sẵn sàng!</div>
        <div class="log-line log-bot">[SYSTEM] Bạn có thể gõ nội dung hoặc dùng các nút lệnh bên dưới.</div>
        <div class="log-line log-sys">--------------------------------------------------</div>
    </div>

    <!-- NÚT ĐIỀU KHIỂN NHANH -->
    <div class="quick-actions">
        <button class="btn-action" onclick="fetch10O5()">💬 10 CÂU O5</button>
        <button class="btn-action" onclick="playGame('PLAYER')">🔵 CƯỢC CON</button>
        <button class="btn-action" onclick="playGame('BANKER')">🔴 CƯỢC CÁI</button>
        <button class="btn-action" style="border-color:#ff5555; color:#ff5555;" onclick="clearTerminal()">🧹 XÓA</button>
    </div>

    <!-- KHUNG CHAT / NHẬP LỆNH -->
    <div class="input-box">
        <span class="prompt-symbol">root@tx68:~#</span>
        <input type="text" id="chat-input" placeholder="Gõ tin nhắn hoặc lệnh..." onkeydown="handleKeyPress(event)">
        <button class="btn-send" onclick="sendChatMessage()">GỬI</button>
    </div>

    <div class="toast" id="toast">ĐÃ COPY!</div>

    <script>
        const Telegram = window.Telegram.WebApp;
        Telegram.expand();

        const rawChat = {{ raw_chat | tojson }};
        const terminal = document.getElementById('terminal');

        function scrollToBottom() {
            terminal.scrollTop = terminal.scrollHeight;
        }

        function showToast(text) {
            const toast = document.getElementById('toast');
            toast.innerText = text;
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 1200);
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                showToast('COPIED: "' + text + '"');
            });
        }

        function getTime() {
            const d = new Date();
            return d.toTimeString().split(' ')[0];
        }

        function appendLog(text, type = 'log-bot') {
            const div = document.createElement('div');
            div.className = 'log-line ' + type;
            div.innerText = `[${getTime()}] ${text}`;
            terminal.appendChild(div);
            scrollToBottom();
        }

        function appendChatBox(text) {
            const div = document.createElement('div');
            div.className = 'log-chat';
            div.innerHTML = `<span>💬 ${text}</span> <span style="float:right; opacity:0.6; font-size:10px;">[NHẤP ĐỂ COPY]</span>`;
            div.onclick = () => copyToClipboard(text);
            terminal.appendChild(div);
            scrollToBottom();
        }

        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const val = input.value.trim();
            if (!val) return;

            appendLog(`USER: ${val}`, 'log-user');
            input.value = '';

            // Tự động phản hồi kiểu Terminal
            setTimeout(() => {
                if (val.toLowerCase() === 'o5') {
                    fetch10O5();
                } else {
                    appendChatBox(val);
                }
            }, 300);
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        }

        function fetch10O5() {
            appendLog('EXECUTE: Get 10 Baccarat Chat Lines...', 'log-sys');
            let shuffled = [...rawChat].sort(() => 0.5 - Math.random()).slice(0, 10);
            shuffled.forEach(s => appendChatBox(s));
        }

        function playGame(choice) {
            appendLog(`BET: ${choice}`, 'log-user');
            const p = Math.floor(Math.random() * 10);
            const b = Math.floor(Math.random() * 10);
            const win = p > b ? 'PLAYER' : (b > p ? 'BANKER' : 'TIE');

            setTimeout(() => {
                appendLog(`RESULT: 🔵 Player: ${p} | 🔴 Banker: ${b}`, 'log-sys');
                if (win === choice) {
                    appendLog(`>> SUCCESS! Bạn đã đoán đúng cửa ${choice}!`, 'log-bot');
                } else if (win === 'TIE') {
                    appendLog(`>> RESULT: Hoà nút!`, 'log-sys');
                } else {
                    appendLog(`>> FAIL! Cửa thắng là ${win}`, 'log-sys');
                }
            }, 400);
        }

        function clearTerminal() {
            terminal.innerHTML = '<div class="log-line log-sys">[SYSTEM] Màn hình đã được làm sạch.</div>';
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, raw_chat=ALL_SENTENCES)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ----------------------------------------------------
# 3. TELEGRAM BOT HANDLER
# ----------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://your-app-name.onrender.com")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "menu"])
@bot.message_handler(func=lambda msg: True)
def handle_all_messages(message):
    markup = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url=RENDER_URL)
    markup.add(InlineKeyboardButton("🖥️ MỞ SẢNH TERMINAL CHAT", web_app=web_app_info))

    msg_text = (
        "<b>[ - TX68 TERMINAL LOBBY - ]</b>\n"
        "<code>═════════════════════════════════════</code>\n"
        "<code>Bấm nút bên dưới để mở Sảnh Chat Terminal</code>\n"
        "<code>màn hình đen, gõ chat & chơi game trực tiếp!</code>\n"
        "<code>═════════════════════════════════════</code>"
    )
    bot.reply_to(message, msg_text, parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Sảnh Terminal đang chạy...")
    bot.infinity_polling()
    
