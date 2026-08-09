import html
import os
import random
import threading
from flask import Flask, render_template_string
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>PHUC TERMINAL LOBBY</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        html, body {
            background-color: #0c0d0e;
            color: #00ff66;
            font-family: 'Consolas', 'Courier New', monospace;
            margin: 0;
            padding: 8px;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
        }

        .app-wrapper {
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
        }

        .header {
            font-size: 10px;
            white-space: pre;
            color: #00e5ff;
            text-align: center;
            line-height: 1.1;
            margin-bottom: 6px;
            user-select: none;
            font-weight: bold;
        }

        .status-bar {
            background: #141619;
            border: 1px solid #22252a;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 11px;
            color: #888;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
            flex-shrink: 0;
        }
        .status-bar span { color: #00ff66; font-weight: bold; }

        /* KHUNG HIỂN THỊ LOG (CÓ THỂ CUỘN) */
        .terminal-window {
            flex: 1;
            background: #050505;
            border: 1px solid #00ff66;
            border-radius: 4px;
            padding: 10px;
            overflow-y: auto;
            font-size: 12px;
            line-height: 1.5;
            margin-bottom: 8px;
            box-shadow: inset 0 0 10px rgba(0, 255, 102, 0.1);
        }

        .log-line {
            margin-bottom: 6px;
            word-break: break-word;
        }

        /* TOOL VIP 7 MÀU CHUYỂN ĐỘNG */
        .tool-vip-rainbow {
            background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8b00ff, #ff0000);
            background-size: 200% auto;
            color: transparent;
            -webkit-background-clip: text;
            background-clip: text;
            animation: rainbow 1.5s linear infinite;
            font-weight: bold;
            display: inline-block;
        }

        @keyframes rainbow {
            0% { background-position: 0% center; }
            100% { background-position: 200% center; }
        }

        .log-chat {
            background: #111;
            border-left: 3px solid #00ff66;
            padding: 8px;
            margin: 6px 0;
            color: #fff;
            border-radius: 3px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .log-chat:active { background: #222; }

        /* KHU VỰC NHẬP DÀNH RIÊNG CHO ĐIỆN THOẠI (TÁCH BIỆT NỔI BẬT) */
        .input-box-wrapper {
            display: flex;
            align-items: center;
            background: #141619;
            border: 1px solid #00ff66;
            border-radius: 4px;
            padding: 4px 8px;
            margin-bottom: 8px;
            flex-shrink: 0;
        }

        .admin-prefix {
            color: #00ff66;
            font-weight: bold;
            font-size: 12px;
            margin-right: 6px;
            white-space: nowrap;
        }

        .input-box-wrapper input {
            flex: 1;
            background: transparent;
            border: none;
            color: #ffffff;
            font-family: inherit;
            font-size: 13px;
            outline: none;
            padding: 8px 0;
            width: 100%;
        }

        .btn-send {
            background: #00ff66;
            color: #000;
            border: none;
            font-weight: bold;
            font-size: 12px;
            padding: 8px 14px;
            border-radius: 3px;
            cursor: pointer;
            margin-left: 6px;
            white-space: nowrap;
        }
        .btn-send:active { background: #00cc52; }

        /* NÚT BẤM THAO TÁC NHANH */
        .quick-actions {
            display: flex;
            gap: 8px;
            flex-shrink: 0;
        }
        .btn-action {
            flex: 1;
            background: #181a1f;
            color: #00e5ff;
            border: 1px solid #00e5ff;
            padding: 12px 0;
            font-family: inherit;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            text-align: center;
        }
        .btn-action:active { background: #00e5ff; color: #000; }
        .btn-danger { border-color: #ff5555; color: #ff5555; flex: 0.4; }
        .btn-danger:active { background: #ff5555; color: #fff; }

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

    <div class="app-wrapper">
        <div class="header">
 ___  _  _ _  _ ____ 
|  _]| || | || |  __|
| |  | || | || | |__ 
|_|  |_||_|____|____|
        </div>

        <div class="status-bar">
            <div>STATUS: <span>ACTIVE</span></div>
            <div>DATABASE: <span style="color:#00e5ff;">100,000+ CÂU</span></div>
        </div>

        <!-- VÙNG HIỂN THỊ LOG CHAT -->
        <div class="terminal-window" id="terminal">
            <div id="logs-container">
                <div class="log-line"><span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#00e5ff;">Chào sếp! Ô chat bên dưới đã sẵn sàng. Gõ lệnh hoặc bấm nút [10 CÂU O5] nhé!</span></div>
                <div class="log-line" style="color:#333;">--------------------------------------------------</div>
            </div>
        </div>

        <!-- VÙNG NHẬP DÀNH RIÊNG - BẤM LÀ NẨY BÀN PHÍM -->
        <div class="input-box-wrapper">
            <span class="admin-prefix">admin:~$</span>
            <input type="text" id="chat-input" placeholder="Gõ câu chat/lệnh tại đây..." autocomplete="off">
            <button class="btn-send" id="btn-submit-chat">GỬI</button>
        </div>

        <div class="quick-actions">
            <button type="button" class="btn-action" id="btn-o5">10 CÂU O5</button>
            <button type="button" class="btn-action btn-danger" id="btn-clear">🧹 XÓA</button>
        </div>
    </div>

    <div class="toast" id="toast">ĐÃ COPY!</div>

    <script>
        const Telegram = window.Telegram.WebApp;
        Telegram.expand();

        const terminal = document.getElementById('terminal');
        const logsContainer = document.getElementById('logs-container');
        const chatInput = document.getElementById('chat-input');
        const btnSubmit = document.getElementById('btn-submit-chat');
        const btnO5 = document.getElementById('btn-o5');
        const btnClear = document.getElementById('btn-clear');

        let isGenerating = false;
        let usedSentences = new Set();

        const xungHo = ["Sếp ơi", "Anh ơi", "Idol ơi", "Đại ca ơi", "Admin ơi", "Sếp lớn", "A ơi", "Chủ phòng", "Sếp VIP", "Idol Baccarat"];
        const napAct = ["mới nạp", "vừa vào vốn", "đã nạp sẵn", "vừa bơm thêm", "em lên vốn", "vừa vào tiền", "mới chuyển cọc"];
        const tienVon = ["500k", "1m", "2m", "3m", "5m", "10m", "15m", "20m", "50m"];
        const trangThai = ["chờ sếp hô lệnh", "chờ sếp lên live", "sẵn sàng chiến rồi", "đợi sếp phát lệnh", "chuẩn bị vào ca", "chờ kéo về bờ"];
        const hupAct = ["vừa húp gọn", "mới bú đậm", "lại cộng thêm", "ăn trọn quả", "đã bú nhẹ", "húp ngọt ngào"];
        const camXuc = ["về bờ rồi sếp", "ấm no quá anh", "uy tín quá sếp", "đẳng cấp quá idol", "ngọt lịm luôn anh", "cảm ơn sếp nhiều"];
        const hoiCau = ["tay này chốt", "ván này đánh", "cầu này bệt", "ván này theo", "tay này bẻ"];
        const cuaDat = ["Banker hay Player", "Con hay Cái", "Con luôn không", "Cái luôn không"];
        const duoiHoi = ["hả sếp ơi", "được không anh", "uy tín không sếp", "nhé đại ca"];

        function generateUniqueBaccaratSentence() {
            let sentence = "";
            let attempts = 0;
            while (attempts < 30) {
                const randType = Math.floor(Math.random() * 3);
                const x = xungHo[Math.floor(Math.random() * xungHo.length)];
                if (randType === 0) {
                    sentence = `${x} ${napAct[Math.floor(Math.random() * napAct.length)]} ${tienVon[Math.floor(Math.random() * tienVon.length)]} ${trangThai[Math.floor(Math.random() * trangThai.length)]}`;
                } else if (randType === 1) {
                    sentence = `${x} ${hupAct[Math.floor(Math.random() * hupAct.length)]} ${tienVon[Math.floor(Math.random() * tienVon.length)]} ${camXuc[Math.floor(Math.random() * camXuc.length)]}`;
                } else {
                    sentence = `${x} ${hoiCau[Math.floor(Math.random() * hoiCau.length)]} ${cuaDat[Math.floor(Math.random() * cuaDat.length)]} ${duoiHoi[Math.floor(Math.random() * duoiHoi.length)]}`;
                }
                if (!usedSentences.has(sentence)) {
                    usedSentences.add(sentence);
                    return sentence;
                }
                attempts++;
            }
            return sentence;
        }

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

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }

        function appendAdminMsg(text) {
            const div = document.createElement('div');
            div.className = 'log-line';
            div.innerHTML = `<span style="color:#00ff66; font-weight:bold;">admin:~$</span> <span style="color:#ffffff;">${escapeHtml(text)}</span>`;
            logsContainer.appendChild(div);
            scrollToBottom();
        }

        function appendToolVipMsg(text) {
            const div = document.createElement('div');
            div.className = 'log-line';
            div.innerHTML = `<span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#00e5ff;">${escapeHtml(text)}</span>`;
            logsContainer.appendChild(div);
            scrollToBottom();
        }

        function appendChatBox(text) {
            const div = document.createElement('div');
            div.className = 'log-chat';
            div.innerHTML = `<div><span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#ffffff;">${escapeHtml(text)}</span></div> <span style="opacity:0.6; font-size:10px; color:#00ff66;">📋 COPY</span>`;
            div.onclick = () => copyToClipboard(text);
            logsContainer.appendChild(div);
            scrollToBottom();
        }

        function processSend() {
            const val = chatInput.value.trim();
            if (!val) return;

            appendAdminMsg(val);
            chatInput.value = '';

            setTimeout(() => {
                if (val.toLowerCase() === 'o5') {
                    fetch10O5();
                } else {
                    appendToolVipMsg(`Đã nhận lệnh "${val}". Sếp bấm nút [10 CÂU O5] để xuất câu kéo ca nhé!`);
                }
            }, 200);
        }

        // BẮT SỰ KIỆN NÚT GỬI VÀ PHÍM ENTER
        btnSubmit.addEventListener('click', processSend);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                processSend();
            }
        });

        // XUẤT 10 CÂU O5 KHI BẤM NÚT
        function fetch10O5() {
            if (isGenerating) return;
            isGenerating = true;
            btnO5.disabled = true;
            btnO5.style.opacity = '0.5';

            appendToolVipMsg('Đang tự động xuất 10 câu O5 không trùng...');

            let count = 0;
            let timer = setInterval(() => {
                if (count < 10) {
                    const sentence = generateUniqueBaccaratSentence();
                    appendChatBox(sentence);
                    count++;
                    btnO5.innerText = `⏳ ĐANG TẠO (${count}/10)...`;
                } else {
                    clearInterval(timer);
                    isGenerating = false;
                    btnO5.disabled = false;
                    btnO5.style.opacity = '1';
                    btnO5.innerText = '10 CÂU O5';
                    appendToolVipMsg('Đã hoàn tất xuất 10 câu O5!');
                }
            }, 800);
        }

        btnO5.addEventListener('click', fetch10O5);

        btnClear.addEventListener('click', function() {
            if (isGenerating) return;
            logsContainer.innerHTML = '<div class="log-line"><span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#00e5ff;">Màn hình đã được dọn sạch!</span></div>';
            scrollToBottom();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

TOKEN = os.environ.get("BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://your-app-name.onrender.com")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "menu"])
@bot.message_handler(func=lambda msg: True)
def handle_all_messages(message):
    markup = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url=RENDER_URL)
    markup.add(InlineKeyboardButton("🖥️ MỞ TOOL VIP TERMINAL", web_app=web_app_info))

    msg_text = (
        "<b>[ - TOOL VIP CASINO TERMINAL - ]</b>\n"
        "<code>═════════════════════════════════════</code>\n"
        "<code>Bấm nút bên dưới để mở Sảnh Chat Terminal</code>\n"
        "<code>Tích hợp kho 100.000+ câu Baccarat không lặp!</code>\n"
        "<code>═════════════════════════════════════</code>"
    )
    bot.reply_to(message, msg_text, parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
    
