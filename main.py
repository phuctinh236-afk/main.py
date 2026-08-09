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
# 2. FLASK WEBAPP - GIAO DIỆN TERMINAL VIP
# ----------------------------------------------------
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
        * { box-sizing: border-box; }
        body {
            background-color: #0c0d0e;
            color: #00ff66;
            font-family: 'Consolas', 'Courier New', monospace;
            padding: 8px;
            margin: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }

        .app-wrapper {
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
        }

        .pc-dots { display: none; }

        @media (min-width: 768px) {
            body {
                justify-content: center;
                align-items: center;
                background-color: #050505;
                padding: 20px;
            }
            .app-wrapper {
                max-width: 800px;
                height: 90vh;
                border: 1px solid #00ff66;
                border-radius: 8px;
                padding: 15px;
                background: #0c0d0e;
                box-shadow: 0 0 25px rgba(0, 255, 102, 0.2);
            }
            .pc-dots {
                display: flex;
                gap: 6px;
                margin-bottom: 10px;
            }
            .dot { width: 12px; height: 12px; border-radius: 50%; }
            .dot-red { background: #ff5f56; }
            .dot-yellow { background: #ffbd2e; }
            .dot-green { background: #27c93f; }
        }

        .header {
            font-size: 10px;
            white-space: pre;
            color: #00e5ff;
            text-align: center;
            line-height: 1.1;
            margin-bottom: 8px;
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
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }
        .status-bar span { color: #00ff66; font-weight: bold; }
        
        /* ADMIN PANEL MÀU XANH LÁ */
        .admin-panel-prefix {
            color: #00ff66 !important;
            font-weight: bold;
            white-space: nowrap;
        }

        /* TOOL VIP 7 MÀU CHUYỂN ĐỘNG LIÊN TỤC */
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
            display: flex;
            flex-direction: column;
        }

        #logs-container {
            display: flex;
            flex-direction: column;
        }

        .log-line {
            margin-bottom: 6px;
            word-break: break-word;
        }

        /* KHUNG CHAT 1-CHẠM THAY TOÀN BỘ 💬 BẰNG TOOL VIP 7 MÀU */
        .log-chat {
            background: #111;
            border-left: 3px solid #00ff66;
            padding: 6px 8px;
            margin: 5px 0;
            color: #fff;
            cursor: pointer;
            border-radius: 2px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .log-chat:active {
            background: #00ff66;
            color: #000;
        }

        /* FORM NHẬP CHAT CHUẨN ĐIỆN THOẠI */
        .inline-input-line {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-top: 6px;
            padding-bottom: 4px;
            width: 100%;
        }

        .inline-input-line input {
            flex: 1;
            background: transparent;
            border: none;
            color: #fff;
            font-family: inherit;
            font-size: 12px;
            outline: none;
            caret-color: #00ff66;
            width: 100%;
        }

        .quick-actions {
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }
        .btn-action {
            flex: 1;
            background: #181a1f;
            color: #00e5ff;
            border: 1px solid #00e5ff;
            padding: 12px 0;
            font-family: inherit;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            text-align: center;
            transition: all 0.2s;
            -webkit-tap-highlight-color: transparent;
        }
        .btn-action:active {
            background: #00e5ff;
            color: #000;
        }
        .btn-danger {
            border-color: #ff5555;
            color: #ff5555;
            flex: 0.4;
        }
        .btn-danger:active {
            background: #ff5555;
            color: #fff;
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

    <div class="app-wrapper">
        <div class="pc-dots">
            <div class="dot dot-red"></div>
            <div class="dot dot-yellow"></div>
            <div class="dot dot-green"></div>
        </div>

        <div class="header">
 ___  _  _ _  _ ____ 
|  _]| || | || |  __|
| |  | || | || | |__ 
|_|  |_||_|____|____|
        </div>

        <div class="status-bar">
            <div>STATUS: <span>ACTIVE</span></div>
            <div>AI BOT: <span>CASINO_AI_V3</span></div>
        </div>

        <!-- MÀN HÌNH TERMINAL CHÁT -->
        <div class="terminal-window" id="terminal">
            <div id="logs-container">
                <div class="log-line"><span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#00e5ff;">Chào sếp! Sảnh Terminal AI Baccarat đã kích hoạt. Sếp gõ câu hỏi hoặc ấn nút [10 CÂU O5] nhé!</span></div>
                <div class="log-line" style="color:#333;">--------------------------------------------------</div>
            </div>

            <!-- FORM GỬI CHAT TƯƠNG THÍCH MỌI BÀN PHÍM ĐIỆN THOẠI -->
            <form class="inline-input-line" onsubmit="handleFormSubmit(event)">
                <span class="admin-panel-prefix">admin panel:</span>
                <input type="text" id="chat-input" placeholder="Gõ câu hỏi/lệnh rồi bấm Enter..." autocomplete="off">
                <button type="submit" style="display: none;"></button>
            </form>
        </div>

        <!-- NÚT ĐIỀU KHIỂN NHANH -->
        <div class="quick-actions">
            <button type="button" class="btn-action" id="btn-o5" onclick="fetch10O5WithDelay()">10 CÂU O5</button>
            <button type="button" class="btn-action btn-danger" onclick="clearTerminal()">🧹 XÓA</button>
        </div>
    </div>

    <div class="toast" id="toast">ĐÃ COPY!</div>

    <script>
        const Telegram = window.Telegram.WebApp;
        Telegram.expand();

        // FIX LỖI JSON TRÊN TELEGRAM WEBAPP
        const rawChat = {{ raw_chat | tojson | safe }};
        const terminal = document.getElementById('terminal');
        const logsContainer = document.getElementById('logs-container');
        let isGenerating = false;

        function scrollToBottom() {
            terminal.scrollTop = terminal.scrollHeight;
        }

        function showToast(text) {
            const toast = document.getElementById('toast');
            toast.innerText = text;
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 1200);
        }

        function copyToClipboard(text, e) {
            if (e) e.stopPropagation();
            navigator.clipboard.writeText(text).then(() => {
                showToast('COPIED: "' + text + '"');
            });
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;")
                       .replace(/</g, "&lt;")
                       .replace(/>/g, "&gt;");
        }

        function appendAdminMsg(text) {
            const div = document.createElement('div');
            div.className = 'log-line';
            div.innerHTML = `<span class="admin-panel-prefix">admin panel:</span> <span style="color:#ffffff;">${escapeHtml(text)}</span>`;
            logsContainer.appendChild(div);
            scrollToBottom();
        }

        function appendToolVipMsg(text) {
            const div = document.createElement('div');
            div.className = 'log-line';
            const formatted = escapeHtml(text).replace(/\n/g, '<br>');
            div.innerHTML = `<span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#00e5ff;">${formatted}</span>`;
            logsContainer.appendChild(div);
            scrollToBottom();
        }

        /* TOÀN BỘ CHAT HIỂN THỊ ĐỀU DÙNG TOOL VIP 7 MÀU (ĐÃ XÓA 💬) */
        function appendChatBox(text) {
            const div = document.createElement('div');
            div.className = 'log-chat';
            div.innerHTML = `<div><span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#ffffff;">${escapeHtml(text)}</span></div> <span style="opacity:0.6; font-size:10px;">📋 COPY</span>`;
            div.onclick = (e) => copyToClipboard(text, e);
            logsContainer.appendChild(div);
            scrollToBottom();
        }

        // ----------------------------------------------------
        // TRÍ TUỆ NHÂN TẠO AI CASINO & HƯỚNG DẪN DÙNG TOOL
        // ----------------------------------------------------
        function getCasinoAiResponse(input) {
            const low = input.toLowerCase().trim();

            if (low.includes('sài') || low.includes('dùng') || low.includes('sử dụng') || low.includes('hướng dẫn') || low.includes('lệnh') || low.includes('help')) {
                return "🎯 HƯỚNG DẪN SỬ DỤNG TOOL VIP:\n" +
                       "1️⃣ Gõ [o5] hoặc bấm nút [10 CÂU O5]: Tool tự xuất 10 câu chat kéo ca Baccarat (mỗi câu cách 1s).\n" +
                       "2️⃣ Gõ nội dung bất kỳ: Tool tạo thẻ Chat 1-chạm để copy cực nhanh quăng vào nhóm.\n" +
                       "3️⃣ Bấm nút [🧹 XÓA]: Dọn dẹp màn hình Terminal.\n" +
                       "4️⃣ Hỏi bất kỳ điều gì: TOOL VIP AI sẽ giải đáp & tư vấn soi cầu 24/7 cho sếp!";
            }

            if (low.includes('soi cầu') || low.includes('baccarat') || low.includes('con hay cái') || low.includes('banker') || low.includes('player') || low.includes('bệt') || low.includes('bẻ')) {
                return "🎰 MẸO SOI CẦU CASINO TỪ TOOL VIP:\n" +
                       "- Cầu bệt (4-5 tay cùng màu): Đu theo Banker/Player tới khi gãy, tuyệt đối không bẻ gấp thếp!\n" +
                       "- Cầu 1-1: Đi đều tay, chốt lãi khi đạt 20-30% vốn.\n" +
                       "- Giữ đầu lạnh, quản lý vốn 1-2-4 là tỷ lệ thắng lên tới 90%!";
            }

            if (low.includes('về bờ') || low.includes('kéo ca') || low.includes('vốn') || low.includes('nạp tiền')) {
                return "💰 Kế hoạch về bờ an toàn:\nSếp chuẩn bị sẵn mức vốn an toàn vào game, theo đúng lệnh quản lý vốn ca kéo. Húp đủ 2M - 5M chốt lãi ngay không tham sếp nhé!";
            }

            if (low.includes('thua') || low.includes('cháy') || low.includes('xui') || low.includes('cay')) {
                return "⚠️ Trong sảnh Casino, tâm lý quyết định 80% chiến thắng! Khi xui sếp nên nghỉ tay 15 phút xả xui. Bình tĩnh quay lại đi đúng kỷ luật sẽ gỡ lại cả vốn lẫn lời!";
            }

            if (low.includes('chào') || low.includes('hi') || low.includes('hello') || low.includes('sếp') || low.includes('admin')) {
                return "🔥 Chào sếp lớn! TOOL VIP AI sẵn sàng cùng sếp chinh phục sảnh Casino hôm nay. Sếp cần soi cầu hay lấy lệnh cứ bảo em!";
            }

            return `🤖 [TOOL VIP AI]: Em đã nhận thông tin "${input}". Dưới góc nhìn chuyên gia Baccarat/Casino thì làm gì cũng cần sự tính toán & quản lý vốn kỷ luật sếp nhé. Sếp cần tư vấn lệnh hay cách dùng tool cứ nhắn em!`;
        }

        // XỬ LÝ SỰ KIỆN SUBMIT FORM (ĐÃ SỬA LỖI ĐIỆN THOẠI)
        function handleFormSubmit(e) {
            e.preventDefault();
            sendChatMessage();
            return false;
        }

        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const val = input.value.trim();
            if (!val) return;

            appendAdminMsg(val);
            input.value = '';

            setTimeout(() => {
                if (val.toLowerCase() === 'o5') {
                    fetch10O5WithDelay();
                } else {
                    const aiReply = getCasinoAiResponse(val);
                    appendToolVipMsg(aiReply);
                }
            }, 300);
        }

        // TẠO 10 CÂU O5 CÁCH NHAU MỖI 1 GIÂY
        function fetch10O5WithDelay() {
            if (isGenerating) return;

            isGenerating = true;
            const btn = document.getElementById('btn-o5');
            btn.disabled = true;
            btn.style.opacity = '0.5';

            appendToolVipMsg('Đang kích hoạt gói 10 câu O5 kéo ca (mỗi câu cách 1s)...');

            let shuffled = [...rawChat].sort(() => 0.5 - Math.random()).slice(0, 10);
            let count = 0;

            let timer = setInterval(() => {
                if (count < shuffled.length) {
                    appendChatBox(shuffled[count]);
                    count++;
                    btn.innerText = `⏳ ĐANG TẠO (${count}/10)...`;
                } else {
                    clearInterval(timer);
                    isGenerating = false;
                    btn.disabled = false;
                    btn.style.opacity = '1';
                    btn.innerText = '10 CÂU O5';
                    appendToolVipMsg('Hoàn tất xuất 10 câu O5 sếp nhé!');
                }
            }, 1000);
        }

        function clearTerminal() {
            if (isGenerating) return;
            logsContainer.innerHTML = '<div class="log-line"><span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#00e5ff;">Màn hình đã được dọn sạch. Sếp cần hỗ trợ gì cứ nhắn nhé!</span></div>';
            scrollToBottom();
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
    markup.add(InlineKeyboardButton("🖥️ MỞ TOOL VIP TERMINAL", web_app=web_app_info))

    msg_text = (
        "<b>[ - TOOL VIP CASINO TERMINAL - ]</b>\n"
        "<code>═════════════════════════════════════</code>\n"
        "<code>Bấm nút bên dưới để mở Sảnh Chat Terminal</code>\n"
        "<code>Tích hợp AI Trợ Lý Casino & Soi Cầu 24/7!</code>\n"
        "<code>═════════════════════════════════════</code>"
    )
    bot.reply_to(message, msg_text, parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Sảnh Terminal TOOL VIP đang chạy...")
    bot.infinity_polling()
    
