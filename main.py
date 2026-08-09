import html
import os
import random
import threading
from flask import Flask, render_template_string
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# ----------------------------------------------------
# 1. FLASK WEBAPP - GIAO DIỆN TERMINAL VIP
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

        /* KHU VỰC NHẬP LỆNH CHỐNG RELOAD TRANG */
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

        .btn-send-mini {
            background: #00ff66;
            color: #000;
            border: none;
            font-weight: bold;
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 3px;
            cursor: pointer;
            white-space: nowrap;
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
            <div>DATABASE: <span style="color:#00e5ff;">100,000+ CÂU</span></div>
        </div>

        <div class="terminal-window" id="terminal">
            <div id="logs-container">
                <div class="log-line"><span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#00e5ff;">Chào sếp! Sảnh AI Terminal Baccarat kho 100.000+ câu đã sẵn sàng. Gõ chat hoặc ấn [10 CÂU O5] nhé!</span></div>
                <div class="log-line" style="color:#333;">--------------------------------------------------</div>
            </div>

            <!-- CHẶN CÁC SỰ KIỆN NGHẼN BÀN PHÍM VÀ RELOAD TRANG -->
            <div class="inline-input-line">
                <span class="admin-panel-prefix">admin panel:</span>
                <input type="text" id="chat-input" placeholder="Gõ tin nhắn rồi ấn Enter hoặc nút GỬI..." autocomplete="off">
                <button type="button" class="btn-send-mini" onclick="sendChatMessage()">GỬI</button>
            </div>
        </div>

        <div class="quick-actions">
            <button type="button" class="btn-action" id="btn-o5" onclick="fetch10O5WithDelay()">10 CÂU O5</button>
            <button type="button" class="btn-action btn-danger" onclick="clearTerminal()">🧹 XÓA</button>
        </div>
    </div>

    <div class="toast" id="toast">ĐÃ COPY!</div>

    <script>
        const Telegram = window.Telegram.WebApp;
        Telegram.expand();

        const terminal = document.getElementById('terminal');
        const logsContainer = document.getElementById('logs-container');
        const chatInput = document.getElementById('chat-input');
        let isGenerating = false;
        let usedSentences = new Set();

        // ----------------------------------------------------
        // THUẬT TOÁN SINH 100.000+ CÂU BACCARAT SIÊU TỰ NHIÊN
        // ----------------------------------------------------
        const xungHo = ["Sếp ơi", "Anh ơi", "Idol ơi", "Đại ca ơi", "Admin ơi", "Sếp lớn", "A ơi", "Chủ phòng", "Sếp VIP", "Idol Baccarat", "Anh trai", "Sếp em"];
        const napAct = ["mới nạp", "vừa vào vốn", "đã nạp sẵn", "vừa bơm thêm", "em lên vốn", "vừa vào tiền", "mới chuyển cọc", "mới bơm vốn", "đã lên cọc", "vừa nạp xong"];
        const tienVon = ["500k", "1m", "2m", "3m", "5m", "10m", "15m", "20m", "30m", "50m", "100m"];
        const trangThai = ["chờ sếp hô lệnh", "chờ sếp lên live", "sẵn sàng chiến rồi", "đợi sếp phát lệnh", "chuẩn bị vào ca", "chờ kéo về bờ", "sẵn sàng cược", "hóng ca kéo quá"];
        
        const hupAct = ["vừa húp gọn", "mới bú đậm", "lại cộng thêm", "ăn trọn quả", "đã bú nhẹ", "húp ngọt ngào", "mới bú ngọt", "đã húp đậm", "lại bú ngọt lịm"];
        const camXuc = ["về bờ rồi sếp", "ấm no quá anh", "uy tín quá sếp", "đẳng cấp quá idol", "ngọt lịm luôn anh", "cảm ơn sếp nhiều", "quá đã sếp ơi", "ấm cạ rồi anh", "chuẩn đét sếp ơi"];
        
        const hoiCau = ["tay này chốt", "ván này đánh", "cầu này bệt", "ván này theo", "tay này bẻ", "ca này chốt", "qua tay này", "quả này bệt"];
        const cuaDat = ["Banker hay Player", "Con hay Cái", "Con luôn không", "Cái luôn không", "Banker được chưa", "Player được chưa", "Con ngọt hơn hay Cái"];
        const duoiHoi = ["hả sếp ơi", "được không anh", "uy tín không sếp", "nhé đại ca", "được chưa idol", "thế sếp ơi", "chưa anh ơi", "ả sếp"];

        function generateUniqueBaccaratSentence() {
            let sentence = "";
            let attempts = 0;

            while (attempts < 50) {
                const randType = Math.floor(Math.random() * 4);
                const x = xungHo[Math.floor(Math.random() * xungHo.length)];

                if (randType === 0) {
                    sentence = `${x} ${napAct[Math.floor(Math.random() * napAct.length)]} ${tienVon[Math.floor(Math.random() * tienVon.length)]} ${trangThai[Math.floor(Math.random() * trangThai.length)]}`;
                } else if (randType === 1) {
                    sentence = `${x} ${hupAct[Math.floor(Math.random() * hupAct.length)]} ${tienVon[Math.floor(Math.random() * tienVon.length)]} ${camXuc[Math.floor(Math.random() * camXuc.length)]}`;
                } else if (randType === 2) {
                    sentence = `${x} ${hoiCau[Math.floor(Math.random() * hoiCau.length)]} ${cuaDat[Math.floor(Math.random() * cuaDat.length)]} ${duoiHoi[Math.floor(Math.random() * duoiHoi.length)]}`;
                } else {
                    const extra = [
                        "lên live chưa sếp ơi hóng quá",
                        "e lên vốn r nè a kéo thôi",
                        "cầu này cái hay con a ơi",
                        "tay này bệt Banker luôn không sếp",
                        "vừa nạp 2m sẵn sàng về bờ",
                        "sếp ơi ca này chốt Con hay Cái",
                        "mới húp 3m ấm no rồi sếp",
                        "theo sếp đúng là uy tín số 1",
                        "bẻ cầu tay này được chưa đại ca",
                        "đợi lệnh sếp từ sáng tới giờ"
                    ];
                    sentence = `${x} ${extra[Math.floor(Math.random() * extra.length)]}`;
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

        /* KHUNG CHAT HOÀN TOÀN DÙNG TOOL VIP 7 MÀU (XÓA SẠCH ICON 💬) */
        function appendChatBox(text) {
            const div = document.createElement('div');
            div.className = 'log-chat';
            div.innerHTML = `<div><span class="tool-vip-rainbow">TOOL VIP:</span> <span style="color:#ffffff;">${escapeHtml(text)}</span></div> <span style="opacity:0.6; font-size:10px;">📋 COPY</span>`;
            div.onclick = (e) => copyToClipboard(text, e);
            logsContainer.appendChild(div);
            scrollToBottom();
        }

        function getCasinoAiResponse(input) {
            const low = input.toLowerCase().trim();

            if (low.includes('sài') || low.includes('dùng') || low.includes('sử dụng') || low.includes('hướng dẫn') || low.includes('lệnh') || low.includes('help')) {
                return "🎯 HƯỚNG DẪN SỬ DỤNG TOOL VIP:\n" +
                       "1️⃣ Gõ [o5] hoặc bấm [10 CÂU O5]: Tool tự xuất 10 câu chat Baccarat không trùng từ kho 100.000 câu (mỗi câu cách 1s).\n" +
                       "2️⃣ Gõ nội dung bất kỳ: Tool tạo thẻ Chat 1-chạm để copy cực nhanh quăng vào nhóm.\n" +
                       "3️⃣ Bấm [🧹 XÓA]: Dọn dẹp màn hình Terminal.\n" +
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

        // BẮT BÀN PHÍM ENTER BẮT BUỘC KHÔNG LOAD LAI TRANG
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendChatMessage();
            }
        });

        function sendChatMessage() {
            const val = chatInput.value.trim();
            if (!val) return;

            appendAdminMsg(val);
            chatInput.value = '';

            setTimeout(() => {
                if (val.toLowerCase() === 'o5') {
                    fetch10O5WithDelay();
                } else {
                    const aiReply = getCasinoAiResponse(val);
                    appendToolVipMsg(aiReply);
                }
            }, 250);
        }

        // TẠO 10 CÂU O5 LẦN LƯỢT MỖI 1 GIÂY
        function fetch10O5WithDelay() {
            if (isGenerating) return;

            isGenerating = true;
            const btn = document.getElementById('btn-o5');
            btn.disabled = true;
            btn.style.opacity = '0.5';

            appendToolVipMsg('Đang kích hoạt gói 10 câu O5 Baccarat từ kho 100.000 câu...');

            let count = 0;
            let timer = setInterval(() => {
                if (count < 10) {
                    const sentence = generateUniqueBaccaratSentence();
                    appendChatBox(sentence);
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
    return render_template_string(HTML_TEMPLATE)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ----------------------------------------------------
# 2. TELEGRAM BOT HANDLER
# ----------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://your-app-name.onrender.com")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "menu"])
@bot.message_handler(func=lambda msg: True)
def handle_all_messages(message):
    markup = InlineKeyboardMarkup()
    w
